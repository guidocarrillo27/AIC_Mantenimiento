from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':'mantenimiento',
        'USER':'postgres',
        'PASSWORD':'Gabcavel_1511',
        'HOST':'localhost',
        'PORT':'5432'
    }
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']


MEDIA_URL = '/media/'
MEDIA_ROOT =  '/home/guido/Proyectos/AIC_Mantenimiento/media'