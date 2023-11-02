from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Meeting(models.Model):
    title = models.CharField(max_length=250,blank=True,null=True)
    discription = models.TextField(blank=True,null = True)
    dateandtime = models.DateTimeField(blank=True,null=True,auto_created=False)

    

class Meeting_Members(models.Model):
    user_id = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    meeting_id = models.ForeignKey(Meeting,blank=True,null=True,on_delete=models.CASCADE)
    meeting_status = models.BooleanField(default=False,blank=True,null=True)






