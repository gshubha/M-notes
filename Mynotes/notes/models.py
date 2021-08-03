from django.db import models

# Create your models here.

class Note(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.CharField(max_length=32)
    head = models.CharField(max_length=32)
    content = models.CharField(max_length=(1 << 20))
    md = models.CharField(max_length=(1 << 20), default='A')
