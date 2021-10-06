from django.db import models

# Create your models here.

class DocClass(models.Model):
    gp = models.CharField(max_length=100)
    date = models.DateTimeField(max_length=100)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    content = models.TextField()


