from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

# 用户信息表
class Ouser(AbstractUser):
    link = models.URLField('个人网址', blank=True, help_text='提示：网址必须填写以http开头的完整形式')
    # 头像
    avatar = ProcessedImageField(upload_to='avatar/%Y/%m/%d',
                                 default='avatar/default.png', # media里面的默认头像
                                 verbose_name='头像',
                                 processors=[ResizeToFill(80, 80)]
                                 )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username











