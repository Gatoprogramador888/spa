"""
Repository para Service (Servicio).
Capa de acceso a datos para servicios del spa.
"""
from config.database import get_db
from dto.service_dto import ServiceCreateDTO, ServiceReadDTO, ServiceDTO
from models.service import Service


class ServiceRepository:
    """
    Repository para gestionar servicios en la base de datos.
    """
    def get_Object_by_public_id(self, service_id: str) -> ServiceReadDTO | None:
        with get_db() as conn:
            row = conn.query(Service).filter(Service.public_code == service_id).first()
            if row:
                service_dto = ServiceDTO.model_validate(row)
                service : ServiceReadDTO = ServiceReadDTO(service_dto)
                return service
        
        return None

    def create_service(self, service_dto: ServiceCreateDTO) -> bool:
        with get_db() as conn:
            service = Service(
                public_code=service_dto.public_code,
                name=service_dto.name,
                cost_cents=service_dto.cost_cents,
                active=service_dto.active
            )
            conn.add(service)
        
        return True
    
    def list_services(self) -> list[ServiceReadDTO]:
        service_dto = []
        with get_db() as conn:
            services = conn.query(Service).all()
            for service in services:
                print(service.name)
                service_dto.append(
                    ServiceReadDTO(service)
                )            
        return service_dto
    
    def delete_service(self, service_id: str) -> bool:
        with get_db() as conn:
            service = conn.query(Service).filter(Service.public_code == service_id).first()
            if service:
                conn.delete(service)
                return True
        return False
    
    def update_service(self, service_id: str, service_dto: ServiceCreateDTO) -> bool:
        with get_db() as conn:
            service = conn.query(Service).filter(Service.public_code == service_id).first()
            if service:
                service.name = service_dto.name
                service.cost_cents = service_dto.cost_cents
                service.active = service_dto.active
                return True
        return False