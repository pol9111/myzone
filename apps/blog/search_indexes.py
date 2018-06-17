# -*- coding: utf-8 -*-
from haystack import indexes
from .models import Article

# 标签的表
class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    views = indexes.IntegerField(model_attr='views')

    # 数据来源是文章
    def get_model(self):
        return Article

    # 获取文章的数据
    def index_queryset(self, using=None):
        return self.get_model().objects.all()

















