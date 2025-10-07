from django.db import models
import uuid
import datetime

# Create your models here.


class Event(models.Model):

    TYPE = [ 
        {'delete', 'Delete'},
        {'modify', 'Modify'},
        {'add', 'Add'},
    ]
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    msg = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    group_id = models.UUIDField(blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)