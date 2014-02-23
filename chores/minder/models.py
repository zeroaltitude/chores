from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User


def week_interval():
    """Sunday, January 14 - Saturday, January 20"""
    today = date.today()
    # normalize this to sunday = 0 from monday = 0
    dateweekday = (today.weekday() + 1) % 7
    sundaylast = today - timedelta(days=dateweekday)
    saturdaynext = today + timedelta(days=(6 - dateweekday))
    return sundaylast, saturdaynext


class Chore(models.Model):
    chore_name = models.CharField(max_length=100)
    chore_value = models.IntegerField(default=0)
    def week_completions(self):
        date1, date2 = week_interval()
        print "looking for completions between %s, %s" % (date1, date2)
        completions = ChoreCompleted.objects.filter(chore=self).filter(complete_date__gte=date1).filter(complete_date__lte=date2)
        return [completion.complete_date for completion in completions]
    def completions_in(self, date1, date2):
        print "looking for completions between %s, %s" % (date1, date2)
        completions = ChoreCompleted.objects.filter(chore=self).filter(complete_date__gte=date1).filter(complete_date__lte=date2)
        return [completion.complete_date for completion in completions]


class ChoreOwner(models.Model):
    chore = models.ForeignKey(Chore)
    owner = models.ForeignKey(User)


class ChoreCompleted(models.Model):
    chore = models.ForeignKey(Chore)
    complete_date = models.DateField(auto_now=True)
    notes = models.CharField(max_length=4096)

