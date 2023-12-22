import os
from pathlib import Path
from django.conf import settings


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
# SECRET_KEY = 'django-insecure-^0&ah8tak4ds+)r)^iy)2e^rm6h$43!9mfsnm7f(neo+%'
# DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

'''
# 로컬 환경에서 실행 시킬 때
FMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/shape_vgg16_process1.h5'
PMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/ensemble_soft_model_poly.h5'
DMODEL_PATH1 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model1.hdf5'
DMODEL_PATH2 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model2.hdf5'
DMODEL_PATH3 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model3.hdf5'
DMODEL_PATH4 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model4.hdf5'
DMODEL_PATH5 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model5.hdf5'
DMODEL_PATH6 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model6.hdf5'
'''


if DEBUG:
    # 로컬 환경 설정
    FMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/shape_vgg16_process1.h5'
    PMODEL_PATH = 'C:/work/pysou/makemeuppro/mainapp/models/ensemble_soft_model_poly.h5'
    DMODEL_PATH1 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model1.hdf5'
    DMODEL_PATH2 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model2.hdf5'
    DMODEL_PATH3 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model3.hdf5'
    DMODEL_PATH4 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model4.hdf5'
    DMODEL_PATH5 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model5.hdf5'
    DMODEL_PATH6 = 'C:/work/pysou/makemeuppro/mainapp/models/scalp_model6.hdf5'

else:
    # Docker 환경 설정
    FMODEL_PATH = '/app/mainapp/models/shape_vgg16_process1.h5'
    PMODEL_PATH = '/app/mainapp/models/ensemble_soft_model_poly.h5'
    DMODEL_PATH1 = '/app/mainapp/models/scalp_model1.hdf5'
    DMODEL_PATH2 = '/app/mainapp/models/scalp_model2.hdf5'
    DMODEL_PATH3 = '/app/mainapp/models/scalp_model3.hdf5'
    DMODEL_PATH4 = '/app/mainapp/models/scalp_model4.hdf5'
    DMODEL_PATH5 = '/app/mainapp/models/scalp_model5.hdf5'
    DMODEL_PATH6 = '/app/mainapp/models/scalp_model6.hdf5'


FMODEL_PATH = os.getenv('FMODEL_PATH', FMODEL_PATH)
PMODEL_PATH = os.getenv('PMODEL_PATH', PMODEL_PATH)
DMODEL_PATH1 = os.getenv('DMODEL_PATH1', DMODEL_PATH1)
DMODEL_PATH2 = os.getenv('DMODEL_PATH2', DMODEL_PATH2)
DMODEL_PATH3 = os.getenv('DMODEL_PATH3', DMODEL_PATH3)
DMODEL_PATH4 = os.getenv('DMODEL_PATH4', DMODEL_PATH4)
DMODEL_PATH5 = os.getenv('DMODEL_PATH5', DMODEL_PATH5)
DMODEL_PATH6 = os.getenv('DMODEL_PATH6', DMODEL_PATH6)

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
        "ENGINE": os.getenv('SQL_ENGINE', 'django.db.backends.mysql'),
        "NAME": os.getenv('SQL_DATABASE', 'makemeupdb'),
        "USER": os.getenv('SQL_USER', 'root'),
        "PASSWORD": os.getenv('SQL_PASSWORD', 'seoho123'),
        "HOST": os.getenv('SQL_HOST', 'mariadb'),
        "PORT": os.getenv('SQL_PORT', '3306'),
        "OPTIONS": {
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
        },
    }
}


# 미디어 파일 설정 (사용자 업로드 파일)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

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
