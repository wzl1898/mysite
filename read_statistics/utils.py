import datetime
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum, Read_Detail
from django.utils import timezone
from django.db.models import Sum

def read_statistic_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_readed" % (ct.model, obj.pk )
    #阅读数 +1
    if not request.COOKIES.get('blog_%s_readed' % obj.pk):
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    #当天阅读数 +1
        date = timezone.now().date()
        read_detail, created = Read_Detail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num += 1
        read_detail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%m/%d"))
        read_details = Read_Detail.objects.filter(content_type=content_type, date=date)
        ret = read_details.aggregate(read_num_sum = Sum('read_num'))
        read_nums.append(ret['read_num_sum'] or 0)
    return dates, read_nums
