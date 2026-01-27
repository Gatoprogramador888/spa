"""
Endpoints para Services (Servicios).
Rutas CRUD para gestión de servicios.
"""
from fastapi import APIRouter, Depends
from dto.service_dto import ServiceDTO
from domain.service_domain import create_service, list_services, delete_service, get_service_by_public_id, update_service
from dependencies import get_service
from repositories.service_repository import ServiceRepository

router = APIRouter(prefix="/api/services", tags=["services"])


# TODO: Implementar endpoints de servicios

#Primero al de agregar

@router.post("/create", status_code=201)
def create_service_api(service_data: ServiceDTO, 
                       repositorie : ServiceRepository = Depends(get_service)):
    #Pedir authentication aquí 
    if create_service(service_data, repositorie):
        return {"message": "Servicio creado exitosamente."}
    return {"message": "Error al crear el servicio."}

@router.get("/list", response_model=list[ServiceDTO])
def list_services_api(repositorie : ServiceRepository = Depends(get_service)):
    return list_services(repositorie)

@router.delete("/delete/{service_id}", status_code=200)
def delete_service_api(service_id: str, 
                       repositorie : ServiceRepository = Depends(get_service)):
    #Pedir authentication aquí
    if delete_service(service_id, repositorie):
        return {"message": "Servicio eliminado exitosamente."}
    return {"message": "Error al eliminar el servicio."}

@router.get("/get/{service_id}", response_model=ServiceDTO | None)
def get_service_api(service_id: str, 
                    repositorie : ServiceRepository = Depends(get_service)):
    return get_service_by_public_id(service_id, repositorie)