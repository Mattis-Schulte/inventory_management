from django.db import models

# Create your models here.


class Raeume(models.Model):
    name = models.CharField(max_length=10, default=None)
    bauabschnitt = models.CharField(max_length=10, default=None)
    etage = models.IntegerField(default=None)


class Geraete_Klasse(models.Model):
    geraete_klasse_name = models.CharField(default=None)
    icon = models.ImageField(upload_to='static/images', default=None)

