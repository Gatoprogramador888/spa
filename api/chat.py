"""
Chat WebSocket endpoints.
TODO: Implementar lógica de chat con WebSockets
"""
from flask import Blueprint

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')


# TODO: Implementar WebSocket /api/chat/connect
# TODO: Implementar lógica de conexión
# TODO: Implementar broadcast de mensajes
# TODO: Implementar desconexión


@chat_bp.route('', methods=['GET'])
def chat_info():
    """
    TODO: Retornar información del chat (estructura básica)
    """
    pass
