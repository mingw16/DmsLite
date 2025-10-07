# accounts/forms.py
from django import forms
from client.models import Client
from django.core.exceptions import ValidationError



class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'hasło'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'powtórz hasło'}), required=True)
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            msg = 'hasła muszą być takie same'
            self.add_error(None, msg)
            raise ValidationError(msg)
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Client.objects.filter(email=email).exists():
            raise ValidationError('User z takim emailem istnieje')
        return email

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        user = Client.objects.create_user(email=email, password=password)
        return user


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'email'}), max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'hasło'}), required=True)



class ResetPasswordEmailForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'forms-control', 'placeholder':'email'}), max_length=150, required=True)

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     pass
class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'hasło'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'powtórz hasło'}), required=True)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            msg = 'hasła muszą być takie same'
            self.add_error(None, msg)
            raise ValidationError(msg)
        return password2