"""
WSGI config for wordmap project.
It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Base directory (same as settings)
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordmap.settings')

application = get_wsgi_application()
# Serve static files through WhiteNoise
application = WhiteNoise(application, root=str(BASE_DIR / 'staticfiles'))