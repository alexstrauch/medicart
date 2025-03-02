"""
ASGI configuration for the MediCart project.

This module configures the Asynchronous Server Gateway Interface (ASGI)
for handling asynchronous web protocols. It exposes the ASGI callable
as a module-level variable named 'application'.

ASGI allows Django to handle WebSocket, HTTP/2, and other async protocols,
making it suitable for real-time applications and modern web features.
This configuration enables the project to be deployed on any ASGI-compliant
server like Daphne or Uvicorn.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicart.settings')

# Initialize ASGI application
application = get_asgi_application()
