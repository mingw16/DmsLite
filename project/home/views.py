from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from files.utils import list_files_by_group
from  groups.utils import get_user_space
# Create your views here.

@login_required
def home(request):
    space = get_user_space(request.user)
    print(space)
    meta = list_files_by_group(space.id)
    notifications = None
    print(meta)
    if not space :
        notifications = ['Coś poszło nie tak, spróbuj ponownie poźniej']
    context={'files':meta, 'group':space, 'notifications':notifications}
    return render( request, 'home.html', context)