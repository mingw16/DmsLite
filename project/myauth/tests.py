from django.test import TestCase
from client.models import Client

# Create your tests here.
class AuthTest(TestCase):

    def EmailVerification(self):

        u1 = Client.objects.create(user)