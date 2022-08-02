from django.db import models

# Create your models here.
class ChatInfo(models.Model):
    _id =  models.AutoField(primary_key=True)
    ChatType = models.TextField()
    ChatRole = models.TextField()
    ChatDate = models.TextField()
    ChatTime = models.TextField()
    ChatFrom = models.TextField()
    ChatPersonal = models.BooleanField()
    Message = models.TextField()

