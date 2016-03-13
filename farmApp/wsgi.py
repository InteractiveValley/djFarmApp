# -*- encoding: utf-8 -*-
"""
WSGI config for farmApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# configuracion solo para heroku
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farmApp.settings")

# configuracion solo para heroku
application = Cling(get_wsgi_application())
application = get_wsgi_application()