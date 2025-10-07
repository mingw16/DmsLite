from django.db import models
import uuid, os, hashlib
from django.utils.timezone import now
# Create your models here.

def file_dir_path(instance, filename):
    return os.path.join('uploads', str(instance.owner_id), str(instance.id))

def file_hash(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eth_id =models.UUIDField(default=uuid.uuid4)
    file = models.FileField(upload_to=file_dir_path)
    name = models.CharField(blank=False, null=True)
    owner_id = models.UUIDField(default=uuid.uuid4, editable=False)
    group_id = models.UUIDField(null=True, editable=True)
    is_archieved = models.BooleanField(default=False)
    permits = models.IntegerField(default=777)
    hash = models.CharField(max_length=256, null=True)
    date = models.DateField(default=now)
    description = models.CharField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.file and not self.hash:
            self.hash = file_hash(self.file)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)
    class Meta:
        verbose_name = "file"
        verbose_name_plural = ("files")