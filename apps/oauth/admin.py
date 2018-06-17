from django.contrib import admin
from .models import Ouser
# Register your models here.

# 后台管理的用户界面设置
@admin.register(Ouser) # 表要在admin后台系统注册下
class OuserAdmin(admin.ModelAdmin):
    # 用户界面 里面的属性的都是表里的
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    # 增加新用户界面
    fieldsets = (
         ('基础信息', {'fields': (('username', 'email'), ('link',))}),
         ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'),
                              'groups', 'user_permissions')}),
         ('重要日期', {'fields': (('last_login', 'date_joined'),)}),
    )
    # 过滤器
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # 搜索器
    search_fields = ('username', 'email')


# ('groups', 'user_permissions',)  后面加 , 是为了表名这是一个列表而不是元祖
