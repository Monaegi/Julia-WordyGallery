from .base import *

# config_secret 경로 설정
config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE)).read()

# WSGI 어플리케이션
WSGI_APPLICATION = 'config.wsgi.deploy.application'

# allowed_hosts setting
DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# static 경로 설정
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root')

# media 경로 설정
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')

# database 설정 - sqlite3 사용
DATABASES = config_secret_deploy['django']['databases']

#  storage 설정
STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'


#### 서버 실행시 콘솔에서 구별용 출력 ####
print('@@@@@@@ DEBUG: ', DEBUG)
print('@@@@@@@ ALLOWED_HOSTS: ', ALLOWED_HOSTS)
