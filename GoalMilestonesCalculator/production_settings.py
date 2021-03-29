import os,sys
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from config import Config as conf
C = conf()
CONFIG = C.config

ALLOWED_HOSTS = ['ec2-18-188-106-185.us-east-2.compute.amazonaws.com']

DATABASES = {
    'default':
        {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': CONFIG['DATABASE_NAME'],
            'USER': CONFIG['DATABASE_USER'],
            'PASSWORD': CONFIG['DATABASE_PASSWORD'],
            'HOST': CONFIG['DATABASE_HOST'],
            'PORT': CONFIG['DATABASE_PORT']
        }
}
# it's going to be activated once the certificate is provided
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True