from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from read_statistics.models import ReadNum, ReadNumExpandMethod
from django.contrib.contenttypes.fields import GenericRelation
from read_statistics.models import Read_Detail
# Create your models here.
class Blogtype(models.Model):
    #博客类型：1对1
    type = models.CharField(max_length = 15)
    def __str__(self):
        return self.type

class Blog(models.Model, ReadNumExpandMethod):
    #博客
    title = models.CharField(max_length = 30)
    content = RichTextUploadingField()
    blog_type = models.ForeignKey(Blogtype, on_delete = models.CASCADE)
    read_detail = GenericRelation(Read_Detail)
    author = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add = True)
    last_update_time = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']