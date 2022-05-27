from django.contrib import admin
from inventory_management.models import MyUser, Raeume, Geraete_Klasse, Geraete, Tickets

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Raeume)
admin.site.register(Geraete_Klasse)
admin.site.register(Geraete)
admin.site.register(Tickets)
