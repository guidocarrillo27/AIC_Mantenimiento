from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'mantenimiento',
        'USER':'postgres',
        'PASSWORD':'Gabcavel_1511',
        'HOST':'localhost',
        'PORT':'5432'
    }
}

STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')