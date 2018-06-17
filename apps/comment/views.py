from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from blog.models import Article
from comment.models import ArticleComment, Notification


user_model = settings.AUTH_USER_MODEL


@login_required # 必须要登入
@require_POST # 必须post请求
def AddcommentView(request):
    if request.is_ajax():
        data = request.POST # POST get都是虚拟的不在表里真实存在的
        new_user = request.user
        new_content = data.get('content')
        article_id = data.get('article_id')
        rep_id = data.get('rep_id')
        the_article = Article.objects.get(id=article_id)


        if not rep_id:
            new_comment = ArticleComment(author=new_user, content=new_content, belong=the_article, parent=None,
                                         rep_to=None)
        else:
            new_rep_to = ArticleComment.objects.get(id=rep_id)
            new_parent = new_rep_to.parent if new_rep_to.parent else new_rep_to
            # 第一次new_rep_to.parent不存在用new_rep_to, 之后都是这个值
            new_comment = ArticleComment(author=new_user, content=new_content, belong=the_article, parent=new_parent,
                                         rep_to=new_rep_to)


        new_comment.save()
        new_point = '#com-' + str(new_comment.id)
        return JsonResponse({'msg': '评论提交成功！', 'new_point': new_point})
    return JsonResponse({'msg': '评论失败！'})


# 消息列表
@login_required
def NotificationView(request, is_read=None):
    '''展示提示消息列表'''
    now_date = datetime.now()
    return render(request, 'comment/notification.html', context={'is_read': is_read, 'now_date': now_date})


# 将一个消息标记为已读
@login_required
@require_POST
def mark_to_read(request):
    '''将一个消息标记为已读'''
    if request.is_ajax():
        data = request.POST
        user = request.user
        id = data.get('id')
        info = get_object_or_404(Notification, get_p=user, id=id)
        info.mark_to_read() # 表里面的方法
        return JsonResponse({'msg': 'mark success'})
    return JsonResponse({'msg': 'miss'})


# 将一个消息删除
@login_required
@require_POST
def mark_to_delete(request):
    '''将一个消息删除'''
    if request.is_ajax():
        data = request.POST
        user = request.user
        id = data.get('id')
        info = get_object_or_404(Notification, get_p=user, id=id)
        info.delete()
        return JsonResponse({'msg': 'delete success'})














