"""
Repository para Service (Servicio).
Capa de acceso a datos para servicios del spa.
"""
from config.database import get_db
from dto.service_dto import ServiceDTO


class ServiceRepository:
    """
    Repository para gestionar servicios en la base de datos.
    """
    def get_Object_by_public_id(self, service_id: str) -> ServiceDTO | None:
        with get_db() as conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM services WHERE public_code = ?", (service_id,))
                row = cursor.fetchone()
                if row:
                    return ServiceDTO(*row)
                return None
            except Exception as e:
                #loging error
                print(f"Error fetching appointment by public_id: {e}")
                return None

        pass
    pass
