from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm
register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    ct = ContentType.objects.get_for_model(obj)
    comment_count = Comment.objects.filter(content_type=ct, object_id=obj.pk).count()
    return comment_count

@register.simple_tag
def get_comment_form(obj):
    ct_str = ContentType.objects.get_for_model(obj).model
    data = {}
    data['reply_comment_id'] = 0
    data['content_type'] = ct_str
    data['object_id'] = obj.pk
    form = CommentForm(initial=data)
    return form

@register.simple_tag
def get_comments(obj):
    ct = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=ct, object_id=obj.pk, parent=None)
    return comments