from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    nickname = models.CharField(max_length=20, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)\

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.has_nickname = has_nickname