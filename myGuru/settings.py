from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-rc*^)+m)l*)8z2@__69n#o2=+u821io^$k=%@h-0+h6yj8kqs8'

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'authentication',
    'videoCarrer',
    'MultipalTestAdd',
    'CareerManagementSystem',
    'CommanFunctions',   
    'tinymce'
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    # ]
}

ROOT_URLCONF = 'myGuru.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
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


WSGI_APPLICATION = 'myGuru.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'sql_mode': 'traditional',
#         },
#         'NAME': 'myguru',               
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': 'localhost', 
#         'PORT': '3306', 
#     },
# }


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# // Paytem intigration
PAYTEM_MERCHANT_KEY = "@fzp_H%SrTa09MJV"
PAYTEM_MID = "zgZiaS95597255328985"



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:3000',
# )

CORS_ALLOW_ALL_ORIGINS = True


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'visheshsolanki12345@gmail.com'
EMAIL_HOST_PASSWORD = 'wvvnshtnrqhmwiwt'

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
LOGIN_REDIRECT_URL = '/profile/'


# STATIC_URL = '/static/'
# MEDIA_URL = '/images/'

# STATICFILES_DIRS = [
#     BASE_DIR / 'static',
#      BASE_DIR / 'frontend/build/static'
# ]

# MEDIA_ROOT = 'static/images'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "My Guru",
    "site_header": "My Guru",
    "site_logo": "CommanFunctions/images/logo.png",
    "site_logo_classes": "img-circle",
    "welcome_sign": "Welcome to the My Guru",
    "copyright": "myGuru Pvt Ltd",
    "search_model": "auth.User",
    "VideoCarrer_avatar": "CommanFunctions/images/act1.png",

    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "My Guru site", "url": "https://my-guru-test.herokuapp.com/", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "videoCarrer"}
    ],
    "show_sidebar": True,
    "navigation_expanded": True,

    "hide_apps": ["Authtoken", "Django_Rest_Passwordreset"],
    "hide_models": [
        "Videocarrer.VideoRating", "Videocarrer.VideoNoView", 
        "Videocarrer.YouTubeVideo", 
        ],
    "order_with_respect_to": ["auth", "Videocarrer",],

    # "custom_links": {
    #     "videoCarrer": [{
    #         "name": "This Video Carrer", 
    #         "url": "make_messages", 
    #         "icon": "fas fa-comments",
    #         "permissions": ["videoCarrer.VideoCarrer"]
    #     }]
    # },

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "videoCarrer": "fas fa-user",
        "videoCarrer.VideoCarrer": "fas fa-video",
    },
     "related_modal_active": False,
}
