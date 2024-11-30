from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os, sys

sys.path.append(os.path.join(BASE_DIR, 'apps'))
sys.path.append(os.path.join(BASE_DIR))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4$m-ek5271*6!8cfv_pw#y4xin^p16al@%f2_o)=c&ryrq3^ky'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'index'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # cors的中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'address_pro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'address_pro.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'address_pro',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'address_admin',
        'PASSWORD': 'address123?',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            # 实际开发建议使用WARNING
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            # 实际开发建议使用ERROR
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小luffyapi
            'filename': os.path.join(os.path.dirname(BASE_DIR), "log", "address.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.exceptions.common_exception_handler',
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SIMPLEUI_INDEX = '/admin'
SIMPLEUI_LOGO = 'https://cdn.huaxinda.top/settings.svg'

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'menu_display': ['用户', '设置', '订单'],  # 开启排序和过滤功能, 不填此字段为默认排序和全部显示, 空列表[] 为全部不显示.
    'dynamic': True,  # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [

        {
            'app': 'index',  # 关联哪个app
            'name': '用户',
            'icon': 'fas fa-user-shield',
            'url': 'index/addressuser'
        },
        {
            'app': 'index',  # 关联哪个app
            'name': '设置',
            'icon': 'fas fa-user-shield',
            'url': 'index/basesettings'
        },
{
            'app': 'index',  # 关联哪个app
            'name': '订单',
            'icon': 'fas fa-user-shield',
            'url': 'index/order'
        },

    ]
}

SIMPLEUI_HOME_INFO = False
SIMPLEUI_ANALYSIS = False

CSRF_TRUSTED_ORIGINS = []

QINIU = False

if QINIU:
    del MEDIA_URL, MEDIA_ROOT
    # 七牛云存储设置
    QINIU_ACCESS_KEY = 'b7wcgi1r3QLqFaCe6OgZ6k-0tNdX5cIZMrAJLJZU'
    QINIU_SECRET_KEY = 'bgRJoYOF1hFMiVBJVTA2qkDDirq_6gRZCff3086I'
    QINIU_BUCKET_NAME = 'flower001'
    QINIU_BUCKET_DOMAIN = 'cdn.huaxinda.top'
    QINIU_SECURE_URL = False
    PREFIX_URL = 'https://'

    # STATIC文件的更改
    # STATIC_URL = QINIU_BUCKET_DOMAIN + '/static/'
    # STATIC_ROOT = 'static'
    # STATICFILES_STORAGE = 'qiniustorage.backends.QiniuStaticStorage'

    # 文件系统更改
    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'

    MEDIA_ROOT = '/media/'
    MEDIA_URL = PREFIX_URL + QINIU_BUCKET_DOMAIN + MEDIA_ROOT

    # print(MEDIA_ROOT, MEDIA_URL)

# 邮箱配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '275876954@qq.com'
EMAIL_HOST_PASSWORD = 'xpzhkoovtzhgbhgc'
DEFAULT_FROM_EMAIL = '275876954@qq.com'

# 跨域
# 跨域问题的中间件
CORS_ORIGIN_ALLOW_ALL = True  # 允许所有域发请求，等同于response["Access-Control-Allow-Origin"] = "*"

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",

)
