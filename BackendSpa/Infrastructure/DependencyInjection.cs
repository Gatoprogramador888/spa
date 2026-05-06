using BackendSpa.Application.Interfaces;
using BackendSpa.Domain.Interface;
using BackendSpa.Infrastructure.Persistance;
using BackendSpa.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Polly;

namespace BackendSpa.Infrastructure
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddInfrastructure(
            this IServiceCollection services,
            IConfiguration configuration)
        {
            services.AddDbContext<AppDbContext>(options =>
                options.UseMySql(
                    configuration.GetConnectionString("DefaultConnection"),
                    ServerVersion.AutoDetect(configuration.GetConnectionString("DefaultConnection"))
                ));

            services.AddScoped<IAppDbContext>(provider =>
                provider.GetRequiredService<AppDbContext>());

            services.AddScoped<ICalculoAnticipo, CalculoAnticipoService>();
            services.AddScoped<INotificacion, TwilioService>();

            services.AddHttpClient<MercadoPagoService>()
            .AddTransientHttpErrorPolicy(policy =>
                policy.WaitAndRetryAsync(3, retryAttempt =>
                TimeSpan.FromSeconds(retryAttempt)  // intento 1→1s, 2→2s, 3→3s
            )
            );

            return services;
        }
    }
}
