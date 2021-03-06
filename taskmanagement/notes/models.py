# Create your models here.
from django.db import models
from datetime import datetime

# Create your models here.
class NotesModel(models.Model):
    user_id = models.CharField(max_length=50)
    project_id = models.CharField(max_length=50,blank=True)
    task_id = models.CharField(max_length=50,blank=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300,default="",blank=True)
    created_at = models.DateTimeField(default=datetime.now(), blank=True)
    updated_at = models.DateTimeField(default=datetime.now(), blank=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    