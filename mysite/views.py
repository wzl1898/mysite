from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from blog.models import Blog
from django.core.cache import cache
from django.db.models import Sum
from django.contrib import auth
from django.urls import reverse
from user.forms import LoginForm, RegForm
from django.contrib.auth.models import User
from django.http import JsonResponse

def get_7_days_hot_data():
    today = timezone.now().date()
    date = today - timezone.timedelta(days=7)
    blogs = Blog.objects.filter(read_detail__date__lte = today, read_detail__date__gt = date).values('id', 'title') \
                .annotate(read_num_sum = Sum('read_detail__read_num')).order_by('-read_num_sum')
    return blogs[:7]
def get_today_hot_blog():
    today = timezone.now().date()
    blogs = Blog.objects.filter(read_detail__date = today).values('id', 'title').annotate(read_num_sum = Sum('read_detail__read_num')).order_by('-read_num_sum')
    return blogs[:7]
def home(request):
    context = {}
    ct = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(ct)
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_data()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
        print("calc")
    else:
        print("use cache")
    context['hot_blogs_for_7_days'] = hot_blogs_for_7_days
    context['hot_blogs_for_today'] = get_today_hot_blog()
    context['read_nums'] = read_nums
    context['dates'] = dates
    return render(request, 'home.html', context)

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def user_info(request):
    context = {}
    return render(request, 'user_info.html', context)