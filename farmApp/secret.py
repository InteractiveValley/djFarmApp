import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PATH_APP = ''

APP_DEBUG = True

DB_ENGINE = 'django.db.backends.sqlite3'
DB_NAME = os.path.join(BASE_DIR, 'db.sqlite3')  # db_farmapp
DB_USER = ''  # richpolis
DB_PASSWORD = ''  # D3m3s1s1@
DB_HOST = ''
DB_PORT = ''

APP_ALLOWED_HOST = ['*']

APP_TIME_ZONE = 'America/Mexico_City'

APP_STATIC_ROOT = '/Users/richpolis/Proyectos/python/farmApp/staticfiles'

APP_EMAIL_HOST = 'smtp.gmail.com'
APP_EMAIL_HOST_USER = 'richpolis@gmail.com'
APP_EMAIL_HOST_PASSWORD = 'sf2YDI01'
APP_EMAIL_PORT = 587
APP_EMAIL_USE_TLS = True
APP_EMAIL_HOST_EMAIL = 'richpolis@gmail.com'

PUSH_APP_ID = '937172cb'
PUSH_SECRET_API_KEY = '44d39da70a02bc45844e465a348b951619d5706d52e8e59c'

APP_PATH_TERMINOS_PDF = '/Users/richpolis/Proyectos/python/farmApp/usuarios/static/terminos.pdf'

APP_OPENPAY_MERCHANT_ID = 'mpoejxraordmyeoi3naf'
APP_OPENPAY_API_KEY = 'sk_6bb08e7da11f44ea9b6bac0401991fa3'
APP_OPENPAY_VERIFY_SSL_CERTS = False
APP_OPENPAY_PRODUCTION = False

APP_GCM_API_KEY = 'AIzaSyAEuZ-hx04dYElzF1IKxhbH4c9qS4eI5MI'