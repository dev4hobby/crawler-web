from django.db import models

# Create your models here.
class WeatherInfo(models.Model):
    location = models.CharField(max_length=64)
    temperature = models.SmallIntegerField()
    difference = models.CharField(max_length=128)
    