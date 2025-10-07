
from django.test import TestCase
from .utils import send_verif_email
from django.template.loader import render_to_string
# Create your tests here.
class EmailTest(TestCase):
    def sendEmail(self):
        result = send_verif_email('/link aktywacyjny', 'ddmslite@gmail.com', ['asmierciak098@gmail.com',])
        print(result)
        self.assertEqual(result, 1)

    def createTemplateMsg(self):
        content = render_to_string('mail/verification_mail.html', {'verif_link':'customlink'})
        print(content)