from django.db import models

# Create your models here.
# id's nicht enthalten
# Geraete_Klasse -> Beispiel: Anzeigegeraete

class Raeume(models.Model):
    name = models.CharField(max_length=10, default=None)
    BA = (
        ('1', '1. Bauabschnitt'),
        ('2', '2. Bauabschnitt'),
    )
    bauabschnitt = models.CharField(choices=BA, max_length=1)
    Geschoss = (
        ('-1', 'Kellergeschoss'),
        ('0', 'Erdgeschoss'),
        ('1', '1. Obergeschoss'),
        ('2', '2. Obergeschoss')
    )
    etage = models.CharField(choices=Geschoss, max_length=2)
    def __str__(self):
        return self.name



class Geraete_Klasse(models.Model):
    #geraete_klasse_name = models.OptionalChoiceField(choices=(
    #    ('Anzeigegerät', 'Anzeigegerät'),
    #    ('Kamera', 'Kamera'),
    #    ('Licht', 'Licht'),
    #    ('Lampe', 'Lampe'),
    #    ('Schalter', 'Schalter'),
    #    ('Wandtür', 'Wandtür'),
    #    ('Wandlampe', 'Wandlampe'),
    #    ('Wandlicht', 'Wandlicht'),
    #    ('Wandtür', 'Wandtür')))
    icon = models.ImageField(upload_to='static/images', default=None)


    #def __str__(self):
    #    return self.geraete_klasse_name


class Geraete(models.Model):
    geraete_name = models.CharField(max_length=30, default=None)
    geraete_status = models.CharField(max_length=10, default=None)
    geraete_kosten = models.IntegerField(default=None)
    geraete_hersteller = models.CharField(max_length=10, default=None)
    geraete_anschaffungsdatum = models.DateField()
    geraete_garantiedauer_start = models.TimeField()
    geraete_garantiedauer_ende = models.TimeField()
    geraete_seriennummer = models.CharField(max_length=50, default=None)
    geraete_garantie_information = models.CharField(max_length=50, default=None)
    geraete_information = models.CharField(max_length=100, default=None)
    #geraete_klasse = models.ForeignKey(Geraete_Klasse, on_delete=models.CASCADE)


    #raeume = models.ForeignKey(Raeume, on_delete=models.CASCADE)
    def __str__(self):
        return self.geraete_name

class Tickets(models.Model):
    #ticket_name = models.CharField(Raeume, on_delete=models.CASCADE)
    ticket_header = models.CharField(max_length=30, default=None)
    ticket_message = models.CharField(max_length=300, default=None)
    #ticket_typ_name = models.ForeignKey(Typ_Name, on_delete=models.CASCADE)

    def __str__(self):
        return self.ticket_header

