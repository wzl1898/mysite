from django.contrib import admin
from.models import ReadNum, Read_Detail
# Register your models here.

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(Read_Detail)
class Read_DetailAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'date', 'content_object')
