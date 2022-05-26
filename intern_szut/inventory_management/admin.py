from django.contrib import admin
from .models import Raeume, Geraete_Klasse, Geraete, Tickets

# Register your models here.
admin.site.register(Raeume)
admin.site.register(Geraete_Klasse)
admin.site.register(Geraete)
admin.site.register(Tickets)

