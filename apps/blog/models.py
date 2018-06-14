from django.conf import settings
from django.db import models
from django.shortcuts import reverse
import emoji, markdown, re

# Create your models here.


# 文章关键词，用来作为SEO中keywords



class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta: # 不显示在表里,引用些方法
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

# 文章标签
class Tag(models.Model):
    name = models.CharField('文章标签', max_length=20)
    slug = models.SlugField(unique=True)
    description = models.TextField('描述', max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来作为SEO中description,长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

        # '''返回当前标签下所有发表的文章列表'''
    def get_article_list(self):
        return Article.objects.filter(tags=self)















