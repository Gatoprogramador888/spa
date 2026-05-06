using BackendSpa.Application.Features.Citas.Querys;
using BackendSpa.Infrastructure;
using BackendSpa.Middlewares;

var builder = WebApplication.CreateBuilder(args);

// Controllers
builder.Services.AddControllers();

// MediatR — escanea todos los handlers de Application
builder.Services.AddMediatR(cfg =>
    cfg.RegisterServicesFromAssembly(typeof(GetCrearCita).Assembly));

// Infrastructure — DbContext, MP, Twilio
builder.Services.AddInfrastructure(builder.Configuration);

// OpenAPI
builder.Services.AddOpenApi();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseMiddleware<ErrorHandlingMiddleware>();

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();