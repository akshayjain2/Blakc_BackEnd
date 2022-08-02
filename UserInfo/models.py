from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserInfo(models.Model):
    _id = models.AutoField(primary_key=True)
    Name = models.TextField()
    emailId = models.TextField()
    teamName = models.TextField()
    empId = models.TextField()
    password = models.TextField()

class UserTeamInfo(models.Model):
    _id =  models.AutoField(primary_key=True)
    Name = models.TextField()
    AssociateTeam =models.TextField()
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []