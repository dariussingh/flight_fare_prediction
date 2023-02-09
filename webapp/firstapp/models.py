from django.db import models

# Create your models here.

class flight_fare(models.Model):
    Airline  = models.IntegerField()
    Source  = models.IntegerField()
    Destination  = models.IntegerField()
    Total_Stops  = models.IntegerField()
    Journey_Day  = models.IntegerField()
    Journey_month  = models.IntegerField()
    Dep_Hour  = models.IntegerField()
    Dep_Min  = models.IntegerField()
    Arrival_Hour  = models.IntegerField()
    Arrival_min  = models.IntegerField()
    Duration_hours  = models.IntegerField()
    Duration_mins  = models.IntegerField()
    Price  = models.IntegerField()
    