import os

import access

from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = access.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ['localhost', 'stanly.statpsy.ru']

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

CALC_APPS = [
    'mann_whitney',
    'wilcox',
    'compare_two',
    'student_ind',
    'correlation',
    'kruskal',
    'w',
    'z',
    'factor_analytic',
    'anova',
    'desc',
]

CALC_NAMES = [
    'mann_whitney',
    'wilcox',
    'compare_two',
    'student_ind',
    'correlation_kendall',
    'correlation_spearman',
    'correlation_pearson',
    'kruskal',
    'w',
    'z',
    'factor_analytic',
    'anova',
    'desc',
]

CALC_NAMES_TRANS = {
    'mann_whitney': 'U-Манна-Уитни',
    'wilcox': 'Т-Вилкоксона',
    'compare_two': 'Т-Стьюдента (для зависимых выборок)',
    'student_ind': 'Т-Стьюдента (для независимых выборок)',
    'correlation_kendall': 'Корреляционный анализ Кендалл',
    'correlation_spearman': 'Корреляционный анализ Спирмен',
    'correlation_pearson': 'Корреляционный анализ Пирсон',
    'kruskal': 'H-Крускалла-Уоллеса',
    'w': 'Шапиро-Уилка',
    'z': 'Колмогорова-Смирнова',
    'factor_analytic': 'Факторный анализ',
    'anova': 'Однофакторный дисперсионный анализ (ANOVA)',
    'desc': 'Описательные статистики',
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',

    'planfix',
    'import_export',
    'robokassa',
    'sitetree',
    'tinymce',

    'mw_calc',
    'lk',

] + CALC_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mw_calc.middleware.CalcMiddleware',
]

ROOT_URLCONF = 'mw_calc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
	    "/home/stanly/ftp/",
        ] + [os.path.join(BASE_DIR, 'tmp', calc, 'html') for calc in CALC_NAMES],
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

WSGI_APPLICATION = 'mw_calc.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'
USE_TZ = True
USE_I18N = True
USE_L10N = True

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# SESSION_COOKIE_AGE = 0
SESSION_SAVE_EVERY_REQUEST = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'src'),
    os.path.join(BASE_DIR, 'dist'),
] 
# + [os.path.join(BASE_DIR, calc + '/', 'static') for calc in CALC_APPS]


STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other
    # 'compressor.finders.CompressorFinder',
]

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'tmp') + '/debug.log',
        },
        'file_planfix': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'tmp') + '/planfix.log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'logfile': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'planfix': {
            'handlers': ['file_planfix'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# calculators settings
# DIRS
JSON_OUT_DIR = 'json/'
HTML_OUT_DIR = 'html/'
DOCX_OUT_DIR = 'docx/'
XLSX_OUT_DIR = 'xlsx/'
SCRIPT_DIR = 'script/'

CALC_INDEX_URL = '/all/'

HOME_DIR = str(Path.home())

HTML_SCRIPT = 'html.Rmd'
DOCX_SCRIPT = 'docx.Rmd'
XLSX_SCRIPT = 'xlsx.R'

MIME_DOCX = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
MIME_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
# MIME_IMG = 'image/jpeg'
# calculators settings

# EMAIL
EMAIL_HOST = 'smtp.timeweb.ru'
EMAIL_HOST_USER = 'info@statpsy.ru'
EMAIL_HOST_PASSWORD = access.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True
EMAIL_PORT = 465

ADMINS = [('jenia0jenia', 'jenia0jenia@mail.ru'), ('stanly', 'online@statpsy.ru')]
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

# Google RECAPTCHA
G_RECAPTCHA_KEY = access.G_RECAPTCHA_KEY
G_RECAPTCHA_URL = 'https://www.google.com/recaptcha/api/siteverify'


# Vk
VK_APP_ID = 6844855
VK_SECRET_KEY = access.VK_SECRET_KEY
VK_ACCESS_TOKEN = access.VK_ACCESS_TOKEN


# Robokassa
ROBOKASSA_LOGIN = access.ROBOKASSA_LOGIN
ROBOKASSA_PASSWORD1 = access.ROBOKASSA_PASSWORD1
ROBOKASSA_PASSWORD2 = access.ROBOKASSA_PASSWORD2
ROBOKASSA_MERCHANT_LOGIN = access.ROBOKASSA_LOGIN
ROBOKASSA_USE_POST = True
ROBOKASSA_STRICT_CHECK = True
ROBOKASSA_TEST_MODE = False
# ROBOKASSA_TEST_FORM_TARGET = '/robokassa/result/'

# ROBOKASSA_EXTRA_PARAMS = ['redirect', 'user', 'calc_name', 'full_price', 'price_type', 'promo', 'payment_methods']
ROBOKASSA_EXTRA_PARAMS = ['redirect', 'user', 'calc_name', 'full_price', 'price_type']

# Для предотвращения затирания кук после POST запроса с робокассы
SESSION_COOKIE_SAMESITE = None
# Но! firefox требует другое значение!


# AllAuth
SITE_ID = 3
LOGIN_URL = f'{CALC_INDEX_URL}accounts/login/'
LOGIN_REDIRECT_URL = f'{CALC_INDEX_URL}accounts/profile/'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/all/'

SOCIALACCOUNT_ADAPTER = 'mw_calc.adapter.SocialAccountAdapter'


# Tilda
TILDA_PROJECT_ID = "1359010"
TILDA_PAGE_ID = "5941350"
TILDA_HEADER_PAGE_ID = "9455861"


# TILDA_FILENAME = "page5941350.html"
TILDA_PUBLIC_KEY = access.TILDA_PUBLIC_KEY
TILDA_SECRET_KEY = access.TILDA_SECRET_KEY
TILDA_API_URL = "http://api.tildacdn.info/v1/getpagefullexport/"
TILDA_STATIC_ROOT = os.path.join(BASE_DIR, 'static_tilda/', 'tilda/')
TILDA_TEMPLATES_ROOT = os.path.join(BASE_DIR, '../../stanly/ftp/tilda/')


#Planfix
PLANFIX_API_KEY = access.PLANFIX_API_KEY
PLANFIX_PRIVATE_KEY = access.PLANFIX_PRIVATE_KEY
PLANFIX_TOKEN = access.PLANFIX_TOKEN
PLANFIX_LOGIN = 'info@statpsy.ru'
PLANFIX_PASSWORD = access.PLANFIX_PASSWORD
PLANFIX_ACCOUNT = 'stat'
PLANFIX_URL = 'https://apiru.planfix.ru/xml/'

PLANFIX_INITIAL = {
    "host": PLANFIX_URL,
    "api_key": PLANFIX_API_KEY,
    "private_key": PLANFIX_PRIVATE_KEY,
    "user": PLANFIX_LOGIN,
    "password": PLANFIX_PASSWORD,
    "account": PLANFIX_ACCOUNT,

    "project_id": '36428', # Stanly project "Stanly - сервис расчета"
    "task_template_id": '1726096', # Stanly template "Задачи для Stanly"

    # Stanly project "Stanly - сервис расчета"
    # Процесс всех задач
    "process_id": "17086",

     # S1 - Регистрация (без оплаты)
     # Статус задачи
    "status_id_1": '114',

    # S2 - Оплата
    # Статус задачи
    "status_id_2": '115',

    # S3 - Оплата
    # Ручные доработки
    "status_id_3": '116',

    # "task_template": '640', # Шаблон задач "Задачи для Stanly"

    # Шаблон контакта: Контакты Stanly
    # По этому шаблону добаляется информация о зарегистрировавшихся пользователях
    "contacts_template": '983',

    # customField id поле для Название критерия
    "custom_data_id": "3776",
    "custom_data_id_order": "3938",

    # справочник Названия критериев
    "handbook_calc_id": "552",

    # список аналитик
    # группа
    "analitic_group_id": "186",

    # аналитика - Доходы
    "analitic_id": "446",

    # Доходы - поле "Сумма"
    "analitic_field_id": "2040",

    # Доходы - поле "Дата"
    # Дата в виде строки в формате дд-мм-гггг или дд-мм-гггг чч:мм
    "analitic_field_id": "2042",

    # Доходы - поле "Описание"
    "analitic_field_id": "2044",


    # test    
    # "task_id": "3854344",
    # "action_id": "12879054",
    # "new_action_id": "14456304",
    # "new_action_id_2": "14460766",
}

PLANFIX_CALCS = {
    'mann_whitney': 9,
    'wilcox': 10,
    'compare_two': 11,
    'student_ind': 12,
    'kruskal': 13,
    'correlation_kendall': 15,
    'correlation_spearman': 16,
    'correlation_pearson': 17,
    'factor_analytic': 20,
    'w': 26,
    'z': 27,
    'anova': 28,
    'desc': 29,
}



# handbook
# {

#     # id  # Название среди калькуляторов       # Название planfix

#     '2': '01 - нормальность распределения',
#     '3': '02 - описательные статистики',
#     '4': '03 - описание процентных распределений',
#     '5': '04 - хи-квадрат пирсона (анализ сопряженности)',
#     '6': '05 - фи-фишера',
#     '7': '06 - мак-намара',
#     '8': '07 - g-критерий знаков',
#     '9': CALC_NAMES['mann_whitney'],            # '08 - манна-уитни',
#     '10': CALC_NAMES['wilcox'],                 # '09 - т-вилкоксона',
#     '11': CALC_NAMES['compare_two'],            # '10 - т-стьюдента для зависимых групп',
#     '12': CALC_NAMES['student_ind'],            # '11 - т-стьюдента для независимых групп',
#     '13': CALC_NAMES['kruskal'],                # '12 - крускалл-уоллес',
#     '14': '13 - дисперсионный анализ',
#     '15': CALC_NAMES['correlation_kendall'],    # '14 - корреляция кендалла',
#     '16': CALC_NAMES['correlation_spearman'],   # '15 - корреляция спирмена',
#     '17': CALC_NAMES['correlation_pearson'],    # '16 - корреляция пирсона',
#     '18': '17 - корреляционная плеяда',
#     '19': '18 - регрессионный анализ',
#     '20': CALC_NAMES['factor_analytic'],        # '19 - факторный анализ',
#     '21': '20 - кластерный анализ',
#     '22': '21 - многомерное шкалирование',
#     '23': '22 - обработка в шкальные',
#     '24': '23 - генерация данных',
#     '25': '24 - логистическая регрессия',
#     '26': CALC_NAMES['w'],                      # '25 - 'шапиро-уилка',
#     '27': CALC_NAMES['z'],                      # '26 - 'колмогорова-смирнова',
#     '28': CALC_NAMES['anova'],                  # '27 - 'anova',
# }

