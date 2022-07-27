from django.db import models

# Create your models here.
class ChatInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    date = models.TextField()
