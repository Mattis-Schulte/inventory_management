from django.contrib import admin
from inventory_management.models import MyUser, Room, DeviceClasses, Device, Ticket

# Register your models here.
admin.site.register(MyUser)
admin.site.register(Room)
admin.site.register(DeviceClasses)
admin.site.register(Device)
admin.site.register(Ticket)
