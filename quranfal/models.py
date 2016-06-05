from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from quran.models import Aya, DistinctWord


class UserAya(models.Model):
    user = models.ForeignKey(User)
    aya = models.ForeignKey(Aya)
    date = models.DateField()


class UserWord(models.Model):
    user = models.ForeignKey(User)
    word = models.ForeignKey(DistinctWord)
    date = models.DateField()

