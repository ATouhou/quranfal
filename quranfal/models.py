import datetime
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from quran.models import Aya, DistinctWord


class List(models.Model):
    name = models.CharField(max_length=50)
    ayas = models.ManyToManyField(Aya, through='UserAya', related_name='lists')
    distinct_words = models.ManyToManyField(DistinctWord, through='UserWord', related_name='lists')

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(User)
    list = models.ForeignKey(List)
    date = models.DateField(blank=True, null=True, auto_now_add=True)

    class Meta:
        abstract=True


class UserAya(UserSubscription):
    aya = models.ForeignKey(Aya, related_name='user_ayas')


class UserWord(UserSubscription):
    distinct_word = models.ForeignKey(DistinctWord, related_name='user_words')
