Plataforma Web para Gestión de Citas de Spa
🎓 Contexto académico

Este proyecto forma parte de un proyecto universitario, cuyo objetivo es aplicar conceptos de:

análisis de negocio

diseño de software

arquitectura backend

integración con servicios externos

El sistema se desarrolla con un enfoque realista, simulando una solución aplicable a un negocio pequeño.

🧠 Descripción del proyecto

La plataforma es una aplicación web orientada al cliente que permite:

Consultar servicios disponibles

Agendar citas de manera autónoma

Confirmar citas mediante un anticipo

Visualizar citas activas

Comunicarse con el spa mediante un chat básico

La operación del spa se gestiona de forma automatizada, reduciendo la necesidad de interacción directa con la plataforma.

🎯 Problema que resuelve

Los spas pequeños suelen gestionar sus citas mediante mensajes o llamadas, lo que genera:

Desorganización de horarios

Falta de control sobre anticipos

Saturación de mensajes

Errores humanos

Este proyecto busca centralizar y automatizar estos procesos en una sola plataforma web.

🧩 Alcance funcional
👤 Cliente

Visualización de servicios

Selección de fecha y horario

Confirmación de cita mediante pago de anticipo

Consulta de citas activas

Chat en tiempo real para dudas rápidas

🏢 Spa

Recepción automática de notificaciones

Confirmación de citas y pagos

Acceso administrativo limitado (backend) para:

visualización de citas del día

atención de mensajes del chat

Nota: el acceso administrativo está diseñado como una funcionalidad mínima y no como un panel de gestión completo.

🏗️ Arquitectura del sistema

El backend está organizado de forma modular:

DTOs: validación y normalización de datos

Domain: reglas de negocio

Repositories: acceso a base de datos

Integrations: conexión con servicios externos

WebSocket: comunicación en tiempo real

Admin (backend): acceso limitado para operaciones del spa

Esta estructura facilita mantenimiento, escalabilidad y claridad del código.

🛠️ Tecnologías

Python

Flask

Base de datos SQL

WebSocket

Integración con pasarela de pago

Integración con mensajería SMS

📈 Evolución prevista

El sistema está preparado para futuras mejoras, tales como:

Interfaz administrativa web

Visualización gráfica de citas del día

Ampliación del chat

Mejoras de seguridad

Escalamiento a mayor volumen de usuarios

🧠 Nota final

Aunque el proyecto se desarrolla en un contexto académico, su diseño busca reflejar buenas prácticas de ingeniería de software, priorizando simplicidad, claridad y automatización.

👨‍💻 Autores

Jared Sair Fernando Márquez Larios

Edgar Alexis García Ruiz

📍 Guadalajara, Jalisco
📅 2026