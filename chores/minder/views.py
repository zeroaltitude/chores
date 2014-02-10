from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

from minder.models import Chore, ChoreCompleted, ChoreOwner

# Create your views here.
def home(request):
    logged_in = False
    chores = []
    if request.user.is_authenticated():
        logged_in = True
        chores = [chore_owned.chore for chore_owned in ChoreOwner.objects.filter(owner=request.user)]
    else:
        if request.POST.get('username', None) is not None:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logged_in = True
    if logged_in:
        template = "minder/loggedin.html"
    else:
        template = "minder/login.html"
    # if this is a post, someone added a completed chore
    if request.POST.get('completed', None) is not None:
        handle_completed(request.POST['completed'], request.user)
    template = loader.get_template(template)
    context = RequestContext(request, {
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


