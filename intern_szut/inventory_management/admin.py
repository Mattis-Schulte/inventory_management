from django.contrib import admin
from .models import Raeume, Geraete_Klasse, Geraete_Typen, Tickets

# Register your models here.
admin.site.register(Raeume)
admin.site.register(Geraete_Klasse)
admin.site.register(Geraete_Typen)
admin.site.register(Tickets)

