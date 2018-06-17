from django.db.models.signals import post_save
from .models import ArticleComment, Notification # 文章的评论和消息推送

# 消息推送的判断  回复的创建者和回复接受者 的一些判断
def notify_handler(sender, instance, created, **kwargs):
    the_article = instance.belong # 文章所属
    create_p = instance.author # 创建者 get_p 提示接收者
    if created:  # 判断是否是第一次生成评论，是的话就做如下判断,后续修改评论不会再次激活信号
        if instance.rep_to: # 如果是一个评论的回复


            '''如果评论是一个回复评论，则同时通知给文章作者和回复的 评论人，如果2者相等，则只通知一次'''
            if the_article.author == instance.rep_to.author: # 如果消息接收者, 文章作者和评论的人是一个人
                get_p = instance.rep_to.author # 接收者 = 评论的人
                if create_p != get_p: # 不是自己给自己回复的话
                    new_notify = Notification(create_p=create_p, get_p=get_p, comment=instance)
                    new_notify.save()        #创建者一直不变        接受在变         # 这个回复

            # 下面都执行, 即文章作者和评论的人不是一个人就给两个人发消息
            else:
                get_p1 = the_article.author # 消息接收者是文章作者
                if create_p != get_p1: # 不是自己给自己回复的话
                    new1 = Notification(create_p=create_p, get_p=get_p1, comment=instance)
                    new1.save()
                get_p2 = instance.rep_to.author # 消息接收者是评论的人
                if create_p != get_p2: # 不是自己给自己回复的话
                    new2 = Notification(create_p=create_p, get_p=get_p2, comment=instance)
                    new2.save()


        else:
            '''如果评论是一个一级评论而不是回复其他评论并且不是作者自评，则直接通知给文章作者'''
            get_p = the_article.author # 接收者=文章作者
            if create_p != get_p: # 如果创建者不等于文章作者
                new_notify = Notification(create_p=create_p, get_p=get_p, comment=instance)
                new_notify.save()

post_save.connect(notify_handler, sender=ArticleComment)






















