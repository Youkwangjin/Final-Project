import os
from pathlib import Path
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY = os.getenv('SECRET_KEY')
# DEBUG = os.getenv('DEBUG') == 'True'
SECRET_KEY = 'django-insecure-^0&ah8tak4ds+)r)^iy)2e^rm6h$43!9mfsnm7f(neo+%'
DEBUG = True
ALLOWED_HOSTS = ['*']

# 로컬 환경에서 실행 시킬 때
FMODEL_PATH = 'C:/Users/user/git/Final-Project/mainapp/models/shape_vgg16_process1'
PMODEL_PATH = 'C:/Users/user/git/Final-Project/mainapp/models/ensemble_soft_model_poly.h5'
DMODEL_PATH1 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model1.hdf5'
DMODEL_PATH2 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model2.hdf5'
DMODEL_PATH3 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model3.hdf5'
DMODEL_PATH4 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model4.hdf5'
DMODEL_PATH5 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model5.hdf5'
DMODEL_PATH6 = 'C:/Users/user/git/Final-Project/mainapp/models/scalp_model6.hdf5'

'''
if DEBUG:
    # 로컬 환경 설정
    FMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/shape_vgg16_process1.h5'
    PMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/ensemble_soft_model_poly.h5'
else:
    # Docker 환경 설정
    FMODEL_PATH = '/app/models/shape_vgg16.h5'
    PMODEL_PATH = '/app/models/personalcolor_ensemble1.h5'

FMODEL_PATH = os.getenv('FMODEL_PATH', FMODEL_PATH)
PMODEL_PATH = os.getenv('PMODEL_PATH', PMODEL_PATH)
'''

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mainapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "makemeuppro.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = "makemeuppro.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "makemeupdb",
        "USER": "root",
        "PASSWORD": "seoho123",
        "HOST": "localhost",
        "PORT": "3307",
    }
}

# 미디어 파일 설정 (사용자 업로드 파일)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
