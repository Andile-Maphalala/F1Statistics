from django.db import models

# Create your models here.
class QaulyClass(models.Model):
    Pos = models.IntegerField(default=0)
    No = models.CharField(max_length=200)
    Driver = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Q1 = models.CharField(max_length=200)
    Q2 = models.CharField(max_length=200)
    Q3 = models.CharField(max_length=200)
    Laps = models.IntegerField(default=0)
    GP = models.CharField(max_length=200)

class DriverClass(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    No = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Abbr = models.CharField(max_length=200)
    img = models.CharField(max_length=200, default='33' )



class ResultClass(models.Model):
    Pos = models.CharField(max_length=200)
    No = models.CharField(max_length=200)
    Driver = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Laps = models.IntegerField(default=0)
    Time = models.CharField(max_length=200)
    Pts = models.IntegerField(default=0)
    GP = models.CharField(max_length=200)

class StartingClass(models.Model):
    Pos = models.CharField(max_length=200)
    No = models.CharField(max_length=200)
    Driver = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Time = models.CharField(max_length=200)
    GP = models.CharField(max_length=200)

class FastesLapClass(models.Model):
    Pos = models.CharField(max_length=200)
    No = models.CharField(max_length=200)
    Driver = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Lap = models.IntegerField(default=0)
    TOD = models.CharField(max_length=200)
    Time = models.CharField(max_length=200)
    AVGSpeed = models.FloatField(default=0)
    GP = models.CharField(max_length=200)

class SprintClass(models.Model):
    Pos = models.CharField(max_length=200)
    No = models.CharField(max_length=200)
    Driver = models.CharField(max_length=200)
    Car = models.CharField(max_length=200)
    Laps = models.IntegerField(default=0)
    Time = models.CharField(max_length=200)
    Pts = models.IntegerField(default=0)
    GP = models.CharField(max_length=200)