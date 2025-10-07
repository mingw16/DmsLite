from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_verif_email(link, from_email, to_email):
    subject = 'Potwierdź swój email'
    html_content = render_to_string("mail/verification_mail.html", {"verif_link":link})
    plain_msg = strip_tags(html_content)
    send_mail(subject=subject, 
               message=plain_msg, 
               from_email=from_email,
               recipient_list=to_email,
               html_message=html_content)


def send_reset_password_email(link, from_email, to_email):
    subject = 'Zresetuje swoje hasło'
    html_content = render_to_string("mail/reset_password.html", {"link":link})
    plain_msg = strip_tags(html_content)
    send_mail(subject=subject, 
               message=plain_msg, 
               from_email=from_email,
               recipient_list=to_email,
               html_message=html_content)
