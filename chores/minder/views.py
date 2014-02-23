from datetime import date, timedelta

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout

from minder.models import Chore, ChoreCompleted, ChoreOwner


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


def home(request):
    logged_in = False
    chores = []
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
        chores = [chore_owned.chore for chore_owned in ChoreOwner.objects.filter(owner=request.user)]
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


