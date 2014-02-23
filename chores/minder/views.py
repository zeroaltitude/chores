from datetime import date, timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from minder.models import Chore, ChoreCompleted, ChoreOwner

ADMINS = ['admin', 'testadmin']


def get_weeks_from_inception():
    """Weeks starting from the earliest chore completed."""
    earliest_date = ChoreCompleted.objects.all().order_by('complete_date')[0].complete_date
    incrementer = timedelta(days=7)
    today = date.today()
    ret = []
    while earliest_date <= (today + incrementer):
        # normalize this to sunday = 0 from monday = 0
        dateweekday = (earliest_date.weekday() + 1) % 7
        sundaylast = earliest_date - timedelta(days=dateweekday)
        saturdaynext = earliest_date + timedelta(days=(6 - dateweekday))
        ret.append((sundaylast, saturdaynext))
        earliest_date += incrementer
    return ret


def get_this_week():
    """Sunday, January 14 - Saturday, January 20"""
    today = date.today()
    # normalize this to sunday = 0 from monday = 0
    dateweekday = (today.weekday() + 1) % 7
    sundaylast = today - timedelta(days=dateweekday)
    saturdaynext = today + timedelta(days=(6 - dateweekday))
    return "%s - %s" % (sundaylast.strftime("%A, %B %d, %Y"), saturdaynext.strftime("%A, %B %d, %Y"))


def logmeout(request):
    logout(request)
    return HttpResponseRedirect("/")


def historical(request):
    if request.user.username not in ADMINS:
        return HttpResponseRedirect("/")
    weeks = []
    # create an iterator that returns week intervals from the earliest chore completion:
    for week in get_weeks_from_inception():
        users = []
        for user in User.objects.all():
            chores = [chore_owned.chore for chore_owned in ChoreOwner.objects.filter(owner=user)]
            totalearned = sum([(chore.chore_value * len(chore.completions_in(week[0], week[1]))) for chore in chores])
            users.append({'username': user.username, 'chores': chores, 'totalearned': totalearned})
        user_week = {
            'start': week[0],
            'end': week[1],
            'start_ui': week[0].strftime("%A, %B %d, %Y"),
            'end_ui': week[1].strftime("%A, %B %d, %Y"),
            'users': users,
        }
        weeks.append(user_week)
    template = loader.get_template("minder/historical.html")
    context = RequestContext(request, {
        'weeks': weeks,
    })
    return HttpResponse(template.render(context))


def home(request):
    logged_in = False
    chores = []
    users = []
    totalearned = 0
    if request.user.is_authenticated():
        logged_in = True
    else:
        if request.POST.get('username', None) is not None:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logged_in = True
    if logged_in:
        if request.user.username in ADMINS:
            for user in User.objects.all():
                chores = [chore_owned.chore for chore_owned in ChoreOwner.objects.filter(owner=user)]
                totalearned = sum([(chore.chore_value * len(chore.week_completions())) for chore in chores])
                users.append({'username': user.username, 'chores': chores, 'totalearned': totalearned})
            template = "minder/admin-loggedin.html"
        else:
            chores = [chore_owned.chore for chore_owned in ChoreOwner.objects.filter(owner=request.user)]
            totalearned = sum([(chore.chore_value * len(chore.week_completions())) for chore in chores])
            template = "minder/loggedin.html"
    else:
        template = "minder/login.html"
    # if this is a post, someone added a completed chore
    if request.POST.get('completed', None) is not None:
        handle_completed(request.POST['completed'], request.user)
    template = loader.get_template(template)
    context = RequestContext(request, {
        'week': get_this_week(),
        'username': request.user.username,
        'chores': chores,
        'users': users,
        'totalearned': totalearned,
    })
    return HttpResponse(template.render(context))


def handle_completed(completed, user):
    # completed_id|note,completed_id|note...
    completes = completed.split(',')
    for complete in completes:
         if len(complete) > 3:
             id_, value = complete.split('|')
             complete_chore(user, id_, value)


def complete_chore(user, id_, value):
    chore = Chore.objects.get(pk=id_)
    completed_chore = ChoreCompleted(chore=chore, notes=value)
    completed_chore.save()


