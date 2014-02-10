from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Chore(models.Model):
    chore_name = models.CharField(max_length=100)
    chore_value = models.IntegerField(default=0)


class ChoreOwner(models.Model):
    chore = models.ForeignKey(Chore)
    owner = models.ForeignKey(User)


class ChoreCompleted(models.Model):
    chore = models.ForeignKey(Chore)
    complete_date = models.DateField(auto_now=True)
    notes = models.CharField(max_length=4096)

