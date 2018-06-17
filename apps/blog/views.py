from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.views import generic
from django.conf import settings
from .models import Article, Tag, Category, Timeline, Silian
from django.core.cache import cache

from markdown.extensions.toc import TocExtension  # 锚点的拓展
import markdown
import time, datetime

from haystack.generic_views import SearchView  # 导入搜索视图
from haystack.query import SearchQuerySet



def goview(request):
    return render(request, 'blog/test.html')


# 文章具体内容
class ArchiveView(generic.ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'articles'
    paginate_by = 200
    paginate_orphans = 50


# 主页，自然排序
class IndexView(generic.ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    # url传了{'sort': 'v'}进来  浏览量排序
    def get_ordering(self):
        ordering = super(IndexView, self).get_ordering()# 获取到类的内容再覆写这个函数
        sort = self.kwargs.get('sort')
        if sort == 'v': # url传了{'sort': 'v'}进来
            return ('-views', '-update_date', '-id')
        return ordering

# 文章的具体内容
class DetailView(generic.DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super(DetailView, self).get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过半小时才重新统计阅览量,作者浏览忽略
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key) # 获取session记录的时间
        if u != obj.author:
            if not is_read_time: # 是不是同一篇文章
                obj.update_views() # 如果不是
                ses[the_key] = time.time() # session记录时间
            else:  # 如果是同一篇文章
                now_time = time.time()
                t = now_time - is_read_time
                if t > 60 * 30:  # 判断是否超过半个小时
                    obj.update_views()
                    ses[the_key] = time.time()

        # 下面的代码中，我选择文章的 ID 和文章更新的日期作为缓存的 key，
        # 这样可以保证当文章更改的时候能够丢弃旧的缓存进而使用新的缓存，而当文章没有更新的时候，
        # 缓存可以一直被调用，知道缓存按照设置的过期时间过期。

        # 使用redis缓存
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S") # 获取文章更新的时间
        md_key = '{}_md_{}'.format(obj.id, ud) # 通过时间和id获取md的key
        cache_md = cache.get(md_key) # 仓库里找有没有这个key
        if cache_md: # 如果有这个key
            md = cache_md # 要转换的内容
        else: # 如果没有建新的
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ]) # 要转换的内容
            cache.set(md_key, md, 60 * 60 * 12) # 设置新的md key
        obj.body = md.convert(obj.body) # 转换要转换的md
        obj.toc = md.toc
        return obj


class CategoryView(generic.ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self): # 排序
        ordering = super(CategoryView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs): # 分类
        queryset = super(CategoryView, self).get_queryset() # 调用父类的 get_queryset 方法获得全部文章列表
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug')) # 使了 slug=self.kwargs.get('slug') 来获取从 URL 捕获的分类 id 值。
        return queryset.filter(category=cate) # 紧接着就对返回的结果调用了 filter 方法来筛选该分类下的全部文章并返回。

    def get_context_data(self, **kwargs):
        context_data = super(CategoryView, self).get_context_data()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章分类'
        context_data['search_instance'] = cate
        return context_data


class TagView(generic.ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)

    def get_ordering(self):
        ordering = super(TagView, self).get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self, **kwargs):
        queryset = super(TagView, self).get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context_data = super(TagView, self).get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context_data['search_tag'] = '文章标签'
        context_data['search_instance'] = tag
        return context_data


def AboutView(request):
    site_date = datetime.datetime.strptime('2018-04-12','%Y-%m-%d')
    return render(request, 'blog/about.html',context={'site_date':site_date})


class TimelineView(generic.ListView):
    model = Timeline
    template_name = 'blog/timeline.html'
    context_object_name = 'timeline_list'


class SilianView(generic.ListView):
    model = Silian
    template_name = 'blog/silian.xml'
    context_object_name = 'badurls'


# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
class MySearchView(SearchView):
    context_object_name = 'search_list'
    paginate_by = getattr(settings, 'BASE_PAGE_BY', None)
    paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    queryset = SearchQuerySet().order_by('-views')
















