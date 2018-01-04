"""
WSGI config for cs401_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cs401_project.settings")

application = get_wsgi_application()


from whitenoise.django import DjangoWhiteNoise

application = WhiteNoise(DjangoWhiteNoise(get_wsgi_application()),root=settings.MEDIA_ROOT,prefix='/media/',
)
