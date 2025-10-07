from django.db import models
import uuid
from client.models import Client
from django.utils.timezone import now
# Create your models here.

#TODO zroibić formularz do tworzneia nowej grupy

class Membership(models.Model):
    ROLE = [
        {'leader', 'Leader'},
        {'moderator', 'Moderator'},
        {'viewer', 'Viewer'},
        {'priv', 'Private'}
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    member = models.ForeignKey(Client,null = True, on_delete=models.CASCADE, related_name='group')
    group = models.ForeignKey('Group',null = True, on_delete=models.CASCADE,related_name="member")
    type = models.CharField(max_length=20, choices=ROLE, default='viewer')

class Group(models.Model):

    TYPE = [
        {'base', 'Base'},
        {'priv', 'Private'},
        {'share', 'Share'}
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(blank=True, null=True)
    creation_date = models.DateField(default=now)
    description = models.CharField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE, default='leader')