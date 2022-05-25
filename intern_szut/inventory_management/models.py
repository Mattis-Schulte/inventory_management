from django.db import models

# Create your models here.
# id's nicht enthalten
# Geraete_Klasse -> Beispiel: Anzeigegeraete

class Raeume(models.Model):
    name = models.CharField(max_length=10, default=None)
    bauabschnitt = models.CharField(max_length=10, default=None)
    etage = models.IntegerField(default=None)
    bemerkung = models.CharField(max_length=100, default=None)



class Geraete_Klasse(models.Model):
    geraete_klasse_name = models.CharField(max_length=10, default=None)
    icon = models.ImageField(upload_to='static/images', default=None)


class Geraete_Typen(models.Model):
#    name = models.CharField(max_length=10, default=None)
#    status = models.CharField(max_length=10, default=None)
#    kosten = models.IntegerField(default=None)
#    hersteller = models.CharField(max_length=10, default=None)
#    anschaffungsdatum = models.DateField(default=None)
#    seriennummer = models.CharField(max_length=50, default=None)
#    garantiedauer = models.IntegerField(default=None)
#    garantie_informations = models.CharField(max_length=50, default=None)
#    geraete_klasse = models.ForeignKey(Geraete_Klasse, on_delete=models.CASCADE)
#    geraete_typen = models.ForeignKey(Geraete_Typen, on_delete=models.CASCADE)
    geraete_typen_name = models.CharField(max_length=10, default=None)
    #geraete_klasse = models.ForeignKey(Geraete_Klasse, on_delete=models.CASCADE)
    #raeume = models.ForeignKey(Raeume, on_delete=models.CASCADE)

class Tickets(models.Model):
    #ticket_name = models.CharField(Raeume, on_delete=models.CASCADE)
    ticket_header = models.CharField(max_length=10, default=None)
    ticket_message = models.CharField(max_length=100, default=None)
    #ticket_typ_name = models.ForeignKey(Typ_Name, on_delete=models.CASCADE)


