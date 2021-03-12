from django.urls import path
from . import views
urlpatterns = [
    path('', views.blog_list, name = 'blog_list'),
    path('<int:blog_pk>', views.blog_detail, name = "blog_detail"),
    path('typedblog/<int:blog_type_pk>', views.typed_blog, name = 'typed_blog'),
    path('datedblog/<int:year>/<int:month>', views.dated_blog, name = 'dated_blog'),
]