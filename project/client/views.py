from django.shortcuts import render
from .forms import SettingsForms
from django.conf import settings
import os
from django.core.files.base import ContentFile
from django.templatetags.static import static
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):

    if request.method == "POST":
        print(request.POST)
        form = SettingsForms(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            address = form.cleaned_data['address']
            description = form.cleaned_data['description']
            avatar = request.POST.get('avatar')
            if name:
                request.user.name = name
            if surname:
                request.user.surname = surname
            if address:
                request.user.address = address
            if description:
                request.user.description = description
            if avatar:
                request.user.avatar = static(f'img/avatars/{avatar}.png')
            
            request.user.save()

    else:
        form = SettingsForms()

    return render(request, 'client/profile.html', {'form':form})