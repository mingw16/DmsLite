
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, ResetPasswordEmailForm, ResetPasswordForm
from django.contrib.auth import login, authenticate, logout
from client.models import Client
from django.http import HttpResponse, Http404
from mail.utils import send_verif_email, send_reset_password_email
import uuid
from base.models import Token
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from groups.models import Group, Membership



def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():   
            user = form.save()
            group = Group.objects.create(type='priv')
            relation = Membership.objects.create(member=user, group=group,type='priv')
            group.save()
            relation.save()
            send_verif_email('/auth/verify/'+str(user.verification_id)+'/'+str(user.user_id),
                             'ddmslite@gmail.com',[user.email,])
           
            return redirect("login") 
    else:
        form = RegistrationForm()

    return render(request, "myauth/registration.html", {"form": form})

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'nie prawidłowe dane logowania')
    else:
        form = LoginForm()

    return render(request, 'myauth/login.html', {'form':form})


def signout(request):
    if not request.user.is_authenticated:
        return redirect('myauth/login')
    logout(request)
    return redirect('home')

def verify(request, verify_id, user_id):
    try:
        user = Client.objects.filter(user_id=str(user_id)).first()
        if user:
            if str(verify_id) == str(user.verification_id):
                user.is_verified = True
                user.save()
                return render(request, 'myauth/authMessage.html', 
                              {'message':'Dziękujemy za potwierdzenie emaila'})
            else:
                return Http404()
        else:
            raise Http404()
    except:
        raise Http404()
    
def get_reset_email(request):
    if request.user.is_authenticated:
        redirect('home')
    if request.method == 'POST':
        form = ResetPasswordEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = Client.objects.filter(email=email).first()
            if not user:
                form.add_error(None, 'Nie istnieje konto z takim email')
                return render(request, 'myauth/resetEmail.html', {'form':form})
            else:
                token_exp_date = timezone.now()+ timedelta(hours=48)
                token_data={'name':'reset_password','exp_date':token_exp_date,'client':user}
                token, new_token = Token.objects.get_or_create(token_data)
                if token:
                    token.delete()
                    new_token = Token.objects.create(name='reset_password',exp_date=token_exp_date, client=user)
                
                link = f'/auth/reset/{new_token.id}/{user.user_id}'
                send_reset_password_email(link, 'ddmslite@gmail.com', [user.email,])
                return render(request, 'myauth/authMessage.html', {'message':'Wysłano link do resetowania hasła na email'})
    else:
        form = ResetPasswordEmailForm()
    return render(request, 'myauth/resetEmail.html', {'form': form})
                

    
def reset_pass(request, token_id, user_id):

    if request.user.is_authenticated:
        redirect('home')
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            token = Token.objects.filter(id=token_id).first()
            if token:
             
             
                if token.exp_date > timezone.now().date() and token.name=='reset_password' :
                    password = form.cleaned_data['password1']
                    user = Client.objects.filter(user_id=str(user_id)).first()
                    if user:
                        if str(user.tokens.filter(name='reset_password').first().id) == str(token.id):
                            user.set_password(password)
                            user.save()
                            token.delete()
                            return render(request, 'myauth/authMessage.html', {'message':'Hasło zresetowane pomyślnie'})
                        else:
                            return Http404("gggg")
                    else:
                        return Http404()
                else:
                    return Http404()
            else:
                return Http404()
    else:
        form = ResetPasswordForm()
    return render(request, 'myauth/ResetPassword.html', {'form': form})
    # wygeneruj formularrz do przypomiania hasla
    # pobierze ten formularz i wyslij maila z linkiem ktory zaweira 

@login_required
def resend_verif_mail(request):
     user = request.user
     user.verification_id = uuid.uuid4()
     user.save()
     send_verif_email('/auth/verify/'+str(user.verification_id)+'/'+str(user.user_id),
                             'ddmslite@gmail.com',[user.email,])
     return redirect('home')
    
    
