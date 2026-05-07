using BackendSpa.Application.Common.Responsive;
using BackendSpa.Application.Features.Notificaciones.DTO;
using BackendSpa.Application.Features.Notificaciones.Querys;
using BackendSpa.Application.Interfaces;
using BackendSpa.Domain;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Twilio.TwiML.Messaging;

namespace BackendSpa.Application.Features.Pagos.Querys
{
    public class ProcesarWebhookHandler : IRequestHandler<ProcesarWebhookCommand, Responsive<bool>>
    {
        private readonly IAppDbContext _db;
        private readonly IPlataformaPago _plataforma;
        private readonly IConfiguration _config;
        private readonly IMediator _mediator;
        private readonly string numeroTelefonicoSpa = string.Empty;

        public ProcesarWebhookHandler(IAppDbContext db, IPlataformaPago plataforma, IConfiguration config, IMediator mediator)
        {
            _db = db;
            _plataforma = plataforma;
            _config = config;
            numeroTelefonicoSpa = _config["NumberPhone:PhoneNumber"]!;
            _mediator = mediator;
        }

        public async Task<Responsive<bool>> Handle(ProcesarWebhookCommand request, CancellationToken cancellationToken)
        {
            var notif = request.Notificacion;


            // 1. Solo procesamos notificaciones de tipo pago
            if (notif.Type != "payment" || notif.Data?.Id is null)
                return new Responsive<bool>(true, "Notificacion ignorada", false);

            // Verificar que el pago no se haya procesado ya
            var pagoExistente = await _db.Pagos
                .AnyAsync(p => p.PaymentId == notif.Data.Id, cancellationToken);

            if (pagoExistente)
            {
                return new Responsive<bool>(true, $"PaymentId {notif.Data.Id} ya procesado", false);
            }

            // 2. Consultar el pago en MP
            var pagoMp = await _plataforma.ObtenerPagoAsync(notif.Data.Id);
            if (pagoMp is null)
                return new Responsive<bool>(false, "No se pudo obtener el pago de MP", false);

            var root = pagoMp.RootElement;

            var extRef = root.TryGetProperty("external_reference", out var er) ? er.GetString() : null;
            var prefId = root.TryGetProperty("preference_id", out var pref) ? pref.GetString() : null;
            var status = root.TryGetProperty("status", out var st) ? st.GetString() : null;

            // 3. Buscar el pago en BD por external_reference o preference_id
            var pago = await _db.Pagos.FirstOrDefaultAsync(p =>
                (extRef != null && p.ExternalReference == extRef) ||
                (prefId != null && p.PreferenceId == prefId),
                cancellationToken);

            if (pago is null)
                return new Responsive<bool>(false, "Pago no encontrado en BD", false);

            // 4. Actualizar datos del pago
            pago.PaymentId = notif.Data.Id;
            pago.Status = status ?? pago.Status;
            pago.CollectionStatus = root.TryGetProperty("status_detail", out var sd) ? sd.GetString() : null;
            pago.PaymentType = root.TryGetProperty("payment_type_id", out var pt) ? pt.GetString() : null;
            pago.ProcessingMode = root.TryGetProperty("processing_mode", out var pm) ? pm.GetString() : null;

            // 5. Actualizar estado de la cita

            var cita = await _db.Citas.
                Include(c => c.Cliente).
                FirstOrDefaultAsync(c => c.IdCita == pago.IdCita, cancellationToken);

            if (cita is not null)
            {
                Cliente cliente = cita.Cliente;
                string Mensaje = string.Empty;
                if (status == "approved")
                {
                    cita.Estado = EstadoCita.Confirmada;

                    string msg = $"El cliente {cliente.Nombre} con numero {cliente.Telefono} aseguro una cita " +
                        $"el dia {cita.Fecha:dd/MM/yyyy} a las {cita.HoraInicio}";

                    //Enviar de que se confirmo al spa
                    NotificacionDto dtoSpa = new()
                    {
                        IdNotificacion = 0,
                        IdCita = cita.IdCita,
                        Destinatario = numeroTelefonicoSpa,
                        Tipo = TipoNotificacion.Duena.ToString(),
                        Mensaje = msg,
                        EnviadoEn = DateTime.UtcNow
                    };
                    
                    await _mediator.Send(new AddNotificacion(dtoSpa), cancellationToken);

                    //Mensaje de que se acepto la cita al cliente y se confirmo
                    Mensaje = $"Tu cita del {cita.Fecha:dd/MM/yyyy} a las {cita.HoraInicio}" +
                        $" ha sido confirmada. ¡Te esperamos!.\n" +
                        $"En caso de desear cancelar solo de click aqui " +
                        $"{_config["MercadoPago:UrlBase"]}/api/citas/cancelarcita/{cita.IdCita}";

                }
                else if (status == "rejected" || status == "cancelled")
                {
                    //Mensaje solo para el usuario de que su cita fue cancelada
                    cita.Estado = EstadoCita.Cancelada;
                    Mensaje = $"Su cita fue cancelada";
                }

                NotificacionDto dtoCliente = new()
                {
                    IdNotificacion = 0,
                    IdCita = cita.IdCita,
                    Destinatario = cita.Cliente.Telefono,
                    Tipo = TipoNotificacion.Cliente.ToString(),
                    Mensaje = Mensaje,
                    EnviadoEn = DateTime.UtcNow
                };

                await _mediator.Send(new AddNotificacion(dtoCliente), cancellationToken);
            }

            return new Responsive<bool>(true, $"Pago procesado: {status}", true);
        }
    }
}
