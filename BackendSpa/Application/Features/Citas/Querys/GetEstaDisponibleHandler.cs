using BackendSpa.Application.Features.Servicios.DTO;
using BackendSpa.Application.Interfaces;
using BackendSpa.Application.Common.Responsive;
using MediatR;
using Microsoft.EntityFrameworkCore;
using BackendSpa.Application.Features.Citas.DTO;

namespace BackendSpa.Application.Features.Citas.Querys
{
    public class GetEstaDisponibleHandler : IRequestHandler<GetEstaDisponibleQuery, Responsive<bool>>
    {
        private readonly IAppDbContext _db;
        private readonly TimeSpan HoraEntrada = new(8, 0, 0), HoraSalida = new(20,0,0);

        public GetEstaDisponibleHandler(IAppDbContext db)
        {
            _db = db;
        }

        public async Task<Responsive<bool>> Handle(GetEstaDisponibleQuery request, CancellationToken cancellationToken)
        {

            if (request.cita.HoraInicio >= HoraEntrada && request.cita.HoraFin <= HoraSalida) return new Responsive<bool>(
                false,"la hora pedida esta fuera de las horas de trabajo",false
                );

            var cita = await _db.Citas.Where(
                c =>
                //Validar el dia
                c.Fecha == request.cita.Fecha && 
                c.HoraInicio < request.cita.HoraFin &&
                c.HoraFin > request.cita.HoraInicio &&
                c.Estado != Domain.EstadoCita.Cancelada).
            Include( c => c.Cliente).Select
            (c => new CitaDto(
            c.IdCita,                                     
            c.IdCliente,                                  
            c.Cliente.Nombre,                              
            c.Fecha,                                      
            c.HoraInicio,                                 
            c.HoraFin,                                     
            c.Estado.ToString(),                          
            c.PrecioTotal,                                
            c.Anticipo                                    
            )).FirstOrDefaultAsync(cancellationToken);

            //Si es nulo si esta disponible
            bool respuesta = cita is null;
            return new Responsive<bool>(true, respuesta ? "hora disponible" : "hora no disponible" , respuesta);
        }
    }
}
