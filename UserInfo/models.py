from django.db import models

# Create your models here.

class UserInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)

