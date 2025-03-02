"""
WSGI configuration for the MediCart project.

This module configures the Web Server Gateway Interface (WSGI)
for production deployment. It exposes the WSGI callable as a
module-level variable named 'application'.

WSGI is the standard interface between Python web applications
and web servers like Apache or Nginx. This configuration enables
the project to be deployed on any WSGI-compliant server.

For more information, see:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicart.settings')

# Initialize WSGI application
application = get_wsgi_application()
