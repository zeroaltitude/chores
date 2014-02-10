from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from minder.models import Chore, ChoreCompleted

# Create your views here.
def home(request):
    logged_in = False
    chores = []
    if request.user.is_authenticated():
        logged_in = True
    else:
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
    return HttpResponse(template.render(template, {'chores': chores}))


def handle_completed(completed, user):
    # completed_id|note,completed_id|note...
    completes = completed.split(',')
    for complete in completes:
         id_, value = complete.split('|')
         complete_chore(user, id_, value)


def complete_chore(user, id_, value):
    chore = Chore.objects.get(pk=id_)
    completed_chore = ChoreCompleted(chore=chore, user=user, note=value)
    completed_chore.save()


