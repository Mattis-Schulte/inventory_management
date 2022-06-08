from django.contrib import admin
from inventory_management.models import MyUser, BuildingSection, Floor, Room, DeviceCategory, DeviceManufacturer, Device, Ticket

# Register your models here.
admin.site.register(MyUser)
admin.site.register(BuildingSection)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(DeviceCategory)
admin.site.register(DeviceManufacturer)
admin.site.register(Device)
admin.site.register(Ticket)
# admin.site.register(TicketComment)
