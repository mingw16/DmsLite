from django.test import TestCase, Client
from django.contib.auth import get_user_model
from django.urls import reverse
from client.models import Client
# Create your tests here.
User = get_user_model()


class HomeViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.home.url = reverse('home')
        self.user = Client.objects.create(email='testemail@gmail.com', password='testpass')
    
    def test_home_view_after_login(self):
        self.client.login(email='testemail@gmail.com', password='testpass')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)