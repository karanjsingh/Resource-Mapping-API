from django.db import models

# Create your models here.
class Project(models.Model):
    projectname = models.CharField(max_length=200)
    taskname = models.CharField(max_length=200)
    empid = models.CharField(max_length=200,blank=True, null=True)
    starttime = models.DateField()
    endtime = models.DateField()

class Resource(models.Model):
    empid = models.CharField(max_length=200)
    skill = models.CharField(max_length=200)
    availstartdate = models.DateField()
    availenddate = models.DateField()
