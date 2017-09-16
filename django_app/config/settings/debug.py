from .base import *

# config_secret 경로 설정
config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

# WSGI 어플리케이션
WSGI_APPLICATION = 'config.wsgi.debug.application'

# allowed_hosts setting
DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

# django_extensions는 debug환경에서만 설치
INSTALLED_APPS.append('django_extensions')

# static 경로 설정
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# media 경로 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# database 설정 - sqlite3 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3')
    }
}

#  storage 설정
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


#### 서버 실행시 콘솔에서 구별용 출력 ####
print('@@@@@@@ DEBUG: ', DEBUG)
print('@@@@@@@ ALLOWED_HOSTS: ', ALLOWED_HOSTS)
