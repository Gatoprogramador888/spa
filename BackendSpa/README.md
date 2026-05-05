---

# Spa Volta Vida — Backend API

Este proyecto es el sistema de backend para la gestión de citas, servicios y pagos del **Spa Volta Vida**. Implementa una arquitectura robusta, escalable y mantenible, diseñada para manejar la lógica de negocio de agendamiento y procesamiento de pagos con Mercado Pago.

## 🚀 Tecnologías (Tech Stack)

* **Runtime:** C# .NET 10
* **API:** ASP.NET Core Web API
* **Database:** MySQL (via EF Core 9 + Pomelo)
* **Arquitectura:** Clean Architecture
* **Patrones:** CQRS con MediatR
* **Validaciones:** FluentValidation
* **Pagos:** Integración nativa con Mercado Pago (vía `HttpClient`, sin SDK)
* **Notificaciones:** Twilio SDK

## 📁 Estructura del Proyecto

El sistema sigue los principios de la **Clean Architecture** para desacoplar la lógica de negocio de la infraestructura:

```text
SpaVoltaVida.sln
├── SpaVoltaVida.Domain         # Entidades, Enums, Interfaces de repositorios
├── SpaVoltaVida.Application    # Casos de uso (Commands/Queries), Validadores, MediatR
├── SpaVoltaVida.Infrastructure # Implementación EF Core, servicios externos (MP, Twilio)
└── SpaVoltaVida.API            # Controladores, Middlewares, Configuración
```

## 🏗️ Arquitectura y Flujos

### CQRS (Command Query Responsibility Segregation)
Utilizamos **MediatR** para separar las operaciones de escritura (Commands) de las de lectura (Queries):
* **Commands:** Manejan la creación, modificación y cancelación de citas. Incluyen validaciones complejas mediante `FluentValidation` antes de persistir.
* **Queries:** Optimizados para la recuperación de datos (servicios, historial, disponibilidad).

### Flujo de Agendamiento
1.  El cliente solicita una cita vía `POST /api/citas`.
2.  `AgendarCitaCommand` valida disponibilidad y traslapes.
3.  Se crea la cita en estado `Pendiente`.
4.  Se genera una preferencia en Mercado Pago (vía `HttpClient`).
5.  Se devuelve la URL de pago al frontend.

### Flujo de Pagos (Webhook)
1.  Mercado Pago notifica el estado del pago al endpoint `POST /api/pagos/webhook`.
2.  El sistema valida la firma y el `external_reference` (ID de la cita).
3.  Se actualiza el estado de la cita a `Confirmada`.
4.  Se dispara el servicio de notificaciones (Twilio) para enviar SMS al cliente y a la dueña.

## 📡 Endpoints Principales

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| **GET** | `/api/servicios` | Obtiene lista de servicios activos agrupados por categoría. |
| **POST** | `/api/citas` | Crea una nueva cita, genera preferencia de pago y retorna URL. |
| **DELETE** | `/api/citas/{id}` | Cancela una cita existente. |
| **GET** | `/api/citas/disponibilidad` | Consulta horarios libres para un día específico. |
| **GET** | `/api/citas/cliente/{email}` | Historial de citas de un cliente. |
| **POST** | `/api/pagos/webhook` | Recepción de notificaciones de estado de pago desde MP. |

## 🛠️ Configuración e Instalación

### Requisitos Previos
* .NET 10 SDK
* MySQL Server (XAMPP o instalado localmente)
* Credenciales de Mercado Pago (Access Token)
* Credenciales de Twilio (SID, Auth Token, From Number)

### Pasos
1.  Clonar el repositorio.
2.  Configurar la cadena de conexión en `appsettings.json`:
    ```json
    "ConnectionStrings": {
        "DefaultConnection": "Server=localhost;Database=spa_volta_vida;Uid=root;Pwd=;"
    }
    ```
3.  Configurar variables de entorno o `appsettings` para los servicios externos:
    * `MercadoPago:AccessToken`
    * `Twilio:AccountSid`, `Twilio:AuthToken`, `Twilio:PhoneNumber`
4.  Ejecutar el proyecto:
    ```bash
    dotnet run --project SpaVoltaVida.API
    ```

## 🛡️ Middlewares
* **ErrorHandlingMiddleware:** Captura excepciones globales y devuelve respuestas JSON estandarizadas.
* **RequestLoggingMiddleware:** Registra la actividad de las peticiones para trazabilidad.

## 📝 Notas de Desarrollo
* **Migraciones:** El esquema de base de datos se maneja manualmente (sin migraciones automáticas) dado que el SQL ya se encuentra definido.
* **Pagos:** Se optó por una implementación directa con `HttpClient` para mantener el proyecto ligero y libre de dependencias externas pesadas (SDK de MP).

---
*Desarrollado para Spa Volta Vida.*