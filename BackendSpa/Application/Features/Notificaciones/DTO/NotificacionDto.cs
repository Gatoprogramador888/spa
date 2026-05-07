namespace BackendSpa.Application.Features.Notificaciones.DTO
{
    public class NotificacionDto
    {
        public int IdNotificacion { get; set; }
        public int IdCita { get; set; }

        // El número de teléfono o correo
        public string Destinatario { get; set; } = string.Empty;

        public string Tipo { get; set; } = string.Empty;

        public string Mensaje { get; set; } = string.Empty;
        public string Status { get; set; } = "pendiente";
        public DateTime? EnviadoEn { get; set; }

        public string? InfoCita { get; set; }
    }
}
