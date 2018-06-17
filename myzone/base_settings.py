# 配置数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 修改数据库为MySQL，并进行配置
        'NAME': 'myzone',
        'USER': 'bridi',
        'PASSWORD': 'qwe123',
        'HOST': '',
        'PORT': 3306,
        'OPTIONS': {'charset': 'utf8mb4', }
    }
}
# 邮箱配置
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # email后端
EMAIL_HOST = 'smtp.163.com' #发送邮件的邮箱 的 SMTP服务器
EMAIL_HOST_USER = 'biscuit36@163.com' #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = '594316'  # 这个不是邮箱密码，而是授权码
EMAIL_PORT = 465  # 由于阿里云的25端口打不开，所以必须使用SSL然后改用465端口
# 是否使用了SSL 或者TLS，为了用465端口，要使用这个
EMAIL_USE_SSL = True
# 默认发件人，不设置的话django默认使用的webmaster@localhost，所以要设置成自己可用的邮箱
DEFAULT_FROM_EMAIL = 'bridi.top <biscuit36@163.com>'
                    # your-webname <your-email@163.com>
# 网站默认设置和上下文信息
SITE_END_TITLE = '网站的名称，如TendCode'
SITE_DESCRIPTION = '网站描述'
SITE_KEYWORDS = '网站关键词，多个词用英文逗号隔开'