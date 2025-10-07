from django.urls import path
from . import views

urlpatterns = [
    path('register', views.signup, name= 'register'),
    path('login', views.signin, name = 'login'),
    path('logout',views.signout, name = 'logout' ),
    path('verify/<uuid:verify_id>/<uuid:user_id>',views.verify, name= 'verify'),
    path('reset',views.get_reset_email, name='email_reset'),
    path('reset/<uuid:token_id>/<uuid:user_id>', views.reset_pass, name='reset_pass'),
    path('resend', views.resend_verif_mail, name='resend')
    ]
