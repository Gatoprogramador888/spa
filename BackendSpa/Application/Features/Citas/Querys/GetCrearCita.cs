using BackendSpa.Application.Common.Responsive;
using BackendSpa.Application.Features.Citas.CitaDetalles.DTO;
using BackendSpa.Application.Features.Citas.CitaDetalles.Querys;
using BackendSpa.Application.Features.Citas.DTO;
using BackendSpa.Application.Features.Clientes.DTO;
using BackendSpa.Application.Features.Clientes.Querys;
using BackendSpa.Application.Features.Pagos.Querys;
using BackendSpa.Application.Features.Servicios.DTO;
using BackendSpa.Application.Features.Servicios.Querys;
using BackendSpa.Application.Interfaces;
using BackendSpa.Domain;
using BackendSpa.Domain.Interface;
using MediatR;

namespace BackendSpa.Application.Features.Citas.Querys
{
    public class GetCrearCita : IRequestHandler<GetCreateCita, Responsive<CitaDto>>
    {
        private readonly IAppDbContext _db;
        private readonly ISender _mediator;
        readonly int horasDepilacion = 120;
        private readonly ICalculoAnticipo _anticipo;


        public GetCrearCita(IAppDbContext db, ISender mediator, ICalculoAnticipo anticipo)
        {
            _db = db;
            _mediator = mediator;
            _anticipo = anticipo;
        }

        public async Task<Responsive<CitaDto>> Handle(GetCreateCita request, CancellationToken cancellationToken)
        {
            var cita = request.cita;
            int tiempo = 0;
            List<ServicioDto> servicios = new();

            //revisar servicios pedidos
            foreach(int id_servicio in cita.IdServicios)
            {
                var servicio = await _mediator.Send(new GetServicioByIdQuery(id_servicio), cancellationToken) ?? 
                    throw new ArgumentException($"el servicio con el id {id_servicio} no existe");

                servicios.Add(servicio);
                tiempo += (int)(servicio.DuracionMin is not null ? servicio.DuracionMin : horasDepilacion);
            }

            TimeSpan horaFinal = cita.HoraInicio.Add(TimeSpan.FromMinutes(tiempo));

            DisponibilidadDTO disponibilidadDTO = new(cita.Fecha, cita.HoraInicio, horaFinal);

            //Ver si esta disponible
            var responsiveDisponibilidad = await _mediator.Send(new GetEstaDisponibleQuery(disponibilidadDTO), cancellationToken);

            if (!responsiveDisponibilidad.Success || !responsiveDisponibilidad.Data) return new Responsive<CitaDto>(
                false,
                responsiveDisponibilidad.Mensaje,
                null
                );

            //Crear precio
            decimal precio = 0;

            foreach(var servicio in servicios)
            {
                precio += servicio.Precio;
            }

            decimal anticipo = _anticipo.Calcular(precio);

            //Request cliente para saber si existe o no
            var EntidadCliente = await _mediator.Send(new GetClienteByName(cita.NombreCliente), cancellationToken);

            int id_cliente = 0;
            var citaDto = request.cita;
            
            if(EntidadCliente.Data is null)
            {
                var cliente = await _mediator.Send(new GetCreateCliente(new ClienteDto(0,
                    citaDto.NombreCliente,
                    citaDto.Email,
                    citaDto.Telefono)), cancellationToken);



                id_cliente = cliente.Data?.IdCliente
                ?? throw new ArgumentException(cliente.Mensaje);
            }
            else
            {
                id_cliente = EntidadCliente.Data.IdCliente;
            }

            Cita entidad = new()
            {
                IdCliente = id_cliente,          
                Fecha = request.cita.Fecha,
                HoraInicio = request.cita.HoraInicio,
                HoraFin = horaFinal,
                Estado = EstadoCita.Pendiente,
                PrecioTotal = precio,        
                Anticipo = anticipo,           
                CreadoEn = DateTime.UtcNow
            };

            await _db.Citas.AddAsync(entidad, cancellationToken);

            await _db.SaveChangesAsync(cancellationToken);

            //Respuesta
            CitaDto dto = new(
                entidad.IdCita,
                id_cliente,
                cita.NombreCliente,
                cita.Fecha,
                cita.HoraInicio,
                horaFinal,
                "pendiente",
                precio,
                anticipo
                );

            //Request de crear Cita Servicio
            List<CitaServicioDto> citaServicioDtos = new();
            foreach (var servicio in servicios)
            {
                CitaServicioDto citaServicioDto = new(0, entidad.IdCita, servicio.IdServicio, servicio.Precio);
                citaServicioDtos.Add(citaServicioDto);
            }

            await _mediator.Send(new GetCitaServicioCreate(citaServicioDtos), cancellationToken);

            var pago = await _mediator.Send(
            new CrearPreferenciaCommand(entidad.IdCita, anticipo),
                cancellationToken
            );

            if (!pago.Success)
            {
                entidad.Estado = EstadoCita.Cancelada;
                await _db.SaveChangesAsync(cancellationToken);
                return new Responsive<CitaDto>(false, pago.Mensaje, null);
            }

            return new Responsive<CitaDto>(true, pago.Data!, dto);
        }
    }
}
