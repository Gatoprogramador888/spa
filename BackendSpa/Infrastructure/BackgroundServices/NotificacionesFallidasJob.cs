using BackendSpa.Application.Features.Notificaciones.DTO;
using BackendSpa.Application.Features.Notificaciones.Querys;
using BackendSpa.Application.Interfaces;
using MediatR;
using Microsoft.EntityFrameworkCore;

namespace BackendSpa.Infrastructure.BackgroundServices
{
    public class NotificacionesFallidasJob : BackgroundService
    {
        private readonly IServiceScopeFactory _scopeFactory;
        private readonly ILogger<NotificacionesFallidasJob> _logger;
        private readonly TimeSpan _intervalo = TimeSpan.FromHours(1);

        public NotificacionesFallidasJob(IServiceScopeFactory scopeFactory, ILogger<NotificacionesFallidasJob> logger)
        {
            _scopeFactory = scopeFactory;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                await ProcesarNotificacionesFallidas(stoppingToken);
                await Task.Delay(_intervalo, stoppingToken);
            }
        }

        private async Task ProcesarNotificacionesFallidas(CancellationToken cancellationToken)
        {
            using var scope = _scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<IAppDbContext>();
            var mediator = scope.ServiceProvider.GetRequiredService<ISender>();

            var notificaciones = await db.Notificaciones
                .Where(n => n.Status == "fallido")
                .ToListAsync(cancellationToken);

            _logger.LogInformation("Notificaciones fallidas a reintentar: {Count}", notificaciones.Count);

            foreach (var notif in notificaciones)
            {
                var resultado = await mediator.Send(new AddNotificacion(new NotificacionDto() {
                    IdCita =notif.IdCita,
                    Destinatario = notif.Destinatario,
                    Tipo = notif.Tipo.ToString(),
                    Mensaje = notif.Mensaje,
                    EnviadoEn = DateTime.UtcNow
                }), cancellationToken);

                _logger.LogInformation("Reintento notificacion {Id}: {Status}",
                    notif.IdNotificacion,
                    resultado.Success ? "exitoso" : "fallido");
            }
        }
    }
}
