"""
Domain para Service (Servicio).
Lógica de negocio relacionada con servicios.
"""
pass

from repositories.service_repository import ServiceRepository
from dto.service_dto import ServiceCreateDTO, ServiceReadDTO, ServiceDTO

def create_service(service_dto: ServiceDTO, repositorie : ServiceRepository) -> bool:
    """
    Lógica para crear un nuevo servicio.
    Valida datos y utiliza el repositorio para persistir.
    """
    service_domain_dto = ServiceCreateDTO.constructo2(service_dto)
    if repositorie.get_Object_by_public_id(service_domain_dto.public_code) is not None:
        raise ValueError("El código público del servicio ya existe.")
    if service_domain_dto.cost_cents < 0:
        raise ValueError("El costo del servicio no puede ser negativo.")
    if not service_domain_dto.name:
        raise ValueError("El nombre del servicio no puede estar vacío.")
    if not service_domain_dto.public_code:
        raise ValueError("El código público del servicio no puede estar vacío.")
    if len(service_domain_dto.public_code) > 50:
        raise ValueError("El código público del servicio no puede exceder 50 caracteres.")
    if len(service_domain_dto.name) > 100:
        raise ValueError("El nombre del servicio no puede exceder 100 caracteres.")
    
    # Aquí se podrían agregar validaciones adicionales si es necesario
    return repositorie.create_service(service_domain_dto)

def list_services(repositorie : ServiceRepository) -> list[ServiceDTO]:
    """
    Lógica para listar todos los servicios.
    Utiliza el repositorio para obtener los datos.
    """
    services_dto = repositorie.list_services()
    services : list[ServiceDTO] = []
    if not services_dto:
        print("No hay servicios disponibles.")
        return []
    for service in services_dto:
        services.append(service.to_BaseDTO())
    return services

def delete_service(service_id: str, repositorie : ServiceRepository) -> bool:
    """
    Lógica para eliminar un servicio por su código público.
    Utiliza el repositorio para realizar la eliminación.
    """
    if repositorie.get_Object_by_public_id(service_id) is not None:
        return repositorie.delete_service(service_id)
    raise ValueError("El servicio con el código público proporcionado no existe.")

def get_service_by_public_id(service_id: str, repositorie : ServiceRepository) -> ServiceDTO | None:
    """
    Lógica para obtener un servicio por su código público.
    Utiliza el repositorio para obtener los datos.
    """
    if service_dto := repositorie.get_Object_by_public_id(service_id):
        return service_dto.to_BaseDTO()
    
    return None

def update_service(service_dto: ServiceDTO, repositorie : ServiceRepository) -> bool:
    """
    Lógica para actualizar un servicio existente.
    Valida datos y utiliza el repositorio para persistir los cambios.
    """
    service_domain_dto = ServiceCreateDTO.constructo2(service_dto)
    if repositorie.get_Object_by_public_id(service_domain_dto.public_code) is None:
        raise ValueError("El servicio con el código público proporcionado no existe.")
    if service_domain_dto.cost_cents < 0:
        raise ValueError("El costo del servicio no puede ser negativo.")
    # Aquí se podrían agregar validaciones adicionales si es necesario
    return repositorie.update_service(service_domain_dto, service_domain_dto)