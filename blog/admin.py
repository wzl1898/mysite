from django.contrib import admin
from .models import Blog, Blogtype
# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_update_time')

@admin.register(Blogtype)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')