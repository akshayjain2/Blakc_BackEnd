from django.db import models


# Create your models here.
class TeamInfo(models.Model):
    _id = models.AutoField(primary_key=True)
    TeamName = models.TextField()
    CreateBy = models.TextField()
    TeamDesc = models.TextField()
    CreatedDate = models.TextField()
    CreatedTime = models.TextField()
    TeamAdmin = models.TextField()

class TeamMember(models.Model):
    _id =  models.AutoField(primary_key=True)
    MembersName = models.TextField()
    TeanName = models.TextField()
    AddBy = models.TextField()
