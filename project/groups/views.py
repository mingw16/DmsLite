from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Group, Membership
from .forms import NewGroupForm
from files.utils import list_files_by_group
from django.http import HttpResponse
from client.models import Client
from timeline.models import Event
from datetime import timedelta
from django.shortcuts import redirect 
from django.http import Http404

from django.db.models.functions import TruncDate
from django.db.models import Count
import traceback
from itertools import groupby
#TODO po nacisnieciu na avatar przenosi do profilu i mozna zrobić follow na profilu

@login_required
def show(request):
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['nazwa']
            description = form.cleaned_data['opis']
            g = Group.objects.create(name=name, description=description, type="base")
            m = Membership.objects.create(member=request.user, group=g,type="leader")
            e = Event.objects.create(email=request.user.email, group_id=g.id, msg=f"stworzył nową grupę", type='add')
            e.save()
            m.save()
            g.save()
    else:
        form = NewGroupForm()
    user_memship = Membership.objects.filter(member=request.user).exclude(type='priv')
    groups = [m.group for m in user_memship]
    data = []
    for group in groups:
        users = Membership.objects.filter(group = group)
        data.append({'group':group,'users':users})

    context = {'data':data, 'form':form}
    return render(request, 'group/home.html', context)


@login_required
def detail(request, group_id):
    group = Group.objects.filter(id = group_id).first()
    files = []
    members = []
    events_data = []
    
    events = Event.objects.filter(group_id=group_id).annotate(temp=TruncDate('date')).values('date','temp','email','msg','type').order_by('-temp')
    for k, v in groupby(events, key=lambda x: x['temp']):
        events_data.append({'date': k, 'obj': list(v)[::-1]} )

    for m in Membership.objects.filter(group=group):
        members.append( {'user':m.member, 'role':m.type, 'mship':m})
    files = list_files_by_group(group.id)
    leader = Membership.objects.filter(group=group, type='leader').first()
    user_role = Membership.objects.filter(group=group, member=request.user).first()
    context = {'group':group, 'members':members, 'files':files, 'leader':leader.member, 'day':events_data, 'role':user_role.type}
    return render(request, 'group/detail.html', context)

@login_required
def add(request):
    if request.method == 'POST':
        group_id = request.POST.get('group')
        email = request.POST.get('email')
        if group_id and email:
            u = Client.objects.filter(email=email).first()
            g = Group.objects.filter(id=group_id).first()
            m = Membership.objects.filter(group=g, member=u).first()
            if not m:
                m = Membership.objects.create(member=u, group=g,type='viewer')
                e = Event.objects.create(email=request.user.email, group_id=g.id, msg=f"dodał nowego użytkownika, < { u.email } >", type='add')
                e.save()
                m.save()
                return redirect('group_detail')
            return redirect('group_detail')
        else:
            return HttpResponse('Taki użytkownik nie istnieje')
    return HttpResponse('')

@login_required
def edit(request):
    if request.method == 'POST':
        try:
            member_id = request.POST.get('member_id')
            member = Membership.objects.filter(id=member_id).first()
            role = request.POST.get('role')
            permission = Membership.objects.filter(group=member.group, member=request.user).first()
            if permission.type == 'leader':
                member.type = role
                e = Event.objects.create(email=request.user.email, group_id=member.group.id, msg=f"zmienił uprawnieni użytkownika { member.member.email } na { role }", type='modify')
                e.save()
                member.save()
                return HttpResponse('Ok')
            else:
                return HttpResponse('not ok')
        except:
            traceback.print_exc()
            return HttpResponse('coś poszło nie tak ')
        
@login_required
def update(request):
    if request.method == 'POST':
        try:
            group_id = request.POST.get('group')
            name = request.POST.get('name')
            description = request.POST.get('description')
            g = Group.objects.filter(id=group_id).first()
            g.name = name
            g.description = description
            g.save()
            e = Event.objects.create(email=request.user.email, group_id=g.group.id, msg=f"zmienił ustawienia grupy",type='modify')
            e.save()
            return HttpResponse('ok')
        except:
            return HttpResponse('coś poszło nie tak') 
        
@login_required
def delete(request, group_id):
    try:
        group = Group.objects.filter(id=group_id).first()
        Membership.objects.filter(group=group).delete()
        Event.objects.filter(group_id=group.id).delete()
        group.delete()
        return redirect('group')
    except:
        return redirect('home')
    

@login_required
def delete_member(request, group_id, email):
    try:
        group = Group.objects.filter(id=group_id).first()
        permission = Membership.objects.filter(group=group, member=request.user, type='leader').first()
        if permission and request.user.email != email:
            client = Client.objects.filter(email=email).first()
            Membership.objects.filter(group=group, member=client).delete()
            e = Event.objects.create(email=request.user.email, group_id=group_id, msg=f"usunał użytkownika {email}",type='delete')
            e.save()
            return redirect('group_detail', group_id=group_id)
        return Http404()
    except:
    
        return Http404()





