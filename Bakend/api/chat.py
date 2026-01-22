"""
Chat WebSocket endpoints.
TODO: Implementar lógica de chat con WebSockets
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["chat"])


# TODO: Implementar WebSocket /api/chat/connect
# TODO: Implementar lógica de conexión
# TODO: Implementar broadcast de mensajes
# TODO: Implementar desconexión


@router.get("")
def chat_info():
    """
    TODO: Retornar información del chat (estructura básica)
    """
    pass
