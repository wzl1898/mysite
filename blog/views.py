from django.shortcuts import render, get_object_or_404
from .models import Blogtype, Blog
from django.core.paginator import Paginator
from django.db.models import Count
from read_statistics.utils import read_statistic_once_read
# Create your views here.

def pagenate(request, blogs):
    page_num = request.GET.get('page', 1)
    cur_page = int(page_num)
    paginator = Paginator(blogs, 2)
    page_num_blogs = paginator.get_page(page_num)
    page_range = list(range(max(cur_page - 2, 1), cur_page)) + list(
        range(cur_page, min(paginator.num_pages, cur_page + 2) + 1))
    if (page_range[0] != 1):
        page_range.insert(0, '...')
        page_range.insert(0, 1)
    if (page_range[-1] != paginator.num_pages):
        page_range.append('...')
        page_range.append(paginator.num_pages)

    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_num_blogs
    context['blog_types'] = Blogtype.objects.annotate(blog_count=Count('blog'))
    '''blog_type_list = []
    blog_types = Blogtype.objects.all()
    for blog_type in blog_types:
        cnt = Blog.objects.filter(blog_type = blog_type).count()
        blog_type.blog_count = cnt
        blog_type_list.append(blog_type)
    context['blog_types'] = blog_type_list'''
    dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in dates:
        blog_count = Blog.objects.filter(created_time__year = blog_date.year, created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs = Blog.objects.all()
    context = pagenate(request, blogs)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    key = read_statistic_once_read(request, blog)
    context = {}
    next_blog = Blog.objects.filter(created_time__gt = blog.created_time).last()
    previous_blog = Blog.objects.filter(created_time__lt = blog.created_time).first()
    context['blog'] = blog
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie(key, 'ture', max_age=60)
    return response

def typed_blog(request, blog_type_pk):
    blog_types = Blogtype.objects.all()
    blog_type = get_object_or_404(Blogtype, pk=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = pagenate(request, blogs)
    context['blog_type_pk'] = blog_type_pk
    context['blog_type'] = blog_type

    return render(request, 'blog/typed_blog.html', context)

def dated_blog(request, year, month):

    blogs = Blog.objects.filter(created_time__year = year, created_time__month = month)
    context = pagenate(request, blogs)
    context['blog_date'] = '%s年%s月' % (year, month)
    context['year'] = year
    context['month'] = month
    return render(request, 'blog/dated_blog.html', context)





