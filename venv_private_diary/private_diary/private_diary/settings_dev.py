from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#ロギング設定
LOGGING = {
    'version':1, #　１固定
    'disable_existing_loggers':False,
    
    #ロガーの設定
    'loggers':{
        #Djangoが利用するロガー
        'django':{
            'handlers':['console'],
            'level':'INFO',
        },
        #diaryアプリケーションが利用するロガー
        'diary':{
            'handlers':['console'],
            'level':'DEBUG',
        },
        
    },
    
    #ハンドラの設定
    'handlers':{
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'dev'
        },
    },
    
    #フォーマッタの設定
    'formatters':{
        'dev':{
            'format':'\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

#メールの配信先を指定 ※開発時はコンソールに設定
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
##メディアファイル関係の設定
#メディアファイルの配置場所
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

