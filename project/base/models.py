from django.db import models
import uuid
from client.models import Client

class Token(models.Model):

    # used token names:
    # reset_password 

    name = models.CharField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    exp_date = models.DateField(default=None)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tokens')

