from django.db import models

# Create your models here.

class UserInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Name = models.TextField()
    emailId = models.TextField()
    teamName = models.TextField()
    empId = models.TextField()
    password = models.TextField()

class UserTeamInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    Name = models.TextField()
    AssociateTeam =models.TextField()
