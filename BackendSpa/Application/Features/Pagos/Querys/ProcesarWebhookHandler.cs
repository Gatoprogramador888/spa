using BackendSpa.Application.Common.Responsive;
using BackendSpa.Application.Interfaces;
using BackendSpa.Domain;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace BackendSpa.Application.Features.Pagos.Querys
{
    public class ProcesarWebhookHandler : IRequestHandler<ProcesarWebhookCommand, Responsive<bool>>
    {
        private readonly IAppDbContext _db;
        private readonly IPlataformaPago _plataforma;
        private readonly INotificacion _notificacion;

        public ProcesarWebhookHandler(IAppDbContext db, IPlataformaPago plataforma, INotificacion notificacion)
        {
            _db = db;
            _plataforma = plataforma;
            _notificacion = notificacion;
        }

        public async Task<Responsive<bool>> Handle(ProcesarWebhookCommand request, CancellationToken cancellationToken)
        {
            var notif = request.Notificacion;

            // 1. Solo procesamos notificaciones de tipo pago
            if (notif.Type != "payment" || notif.Data?.Id is null)
                return new Responsive<bool>(true, "Notificacion ignorada", false);

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
            var cita = await _db.Citas.FindAsync(pago.IdCita, cancellationToken);

            if (cita is not null)
            {
                if (status == "approved")
                {
                    cita.Estado = EstadoCita.Confirmada;
                    await _notificacion.EnviarMensajeAsync(cita.Cliente.Telefono, "tu cita fue confirmada");
                }
                else if (status == "rejected" || status == "cancelled")
                    cita.Estado = EstadoCita.Cancelada;
            }

            await _db.SaveChangesAsync(cancellationToken);

            return new Responsive<bool>(true, $"Pago procesado: {status}", true);
        }
    }
}
