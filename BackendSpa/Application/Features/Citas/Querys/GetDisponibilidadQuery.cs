using BackendSpa.Application.Features.Servicios.DTO;
using MediatR;
using BackendSpa.Application.Common.Responsive;

namespace BackendSpa.Application.Features.Citas.Querys
{
    public record GetEstaDisponibleQuery(CitaDto cita) : IRequest<Responsive<bool>>;
}
