import csv
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from inventory_management.models import MyUser, BuildingSection, Floor, Room, DeviceCategory, DeviceManufacturer, Device, Ticket


class ExportAsCSV:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row_data = ['unknown' if (field is None or field == '') else field for field in [getattr(obj, field) for field in field_names]]
            row = writer.writerow(row_data)

        return response

    export_as_csv.short_description = _('Als CSV exportieren')


# Register your models here.
admin.site.register(MyUser)
admin.site.register(BuildingSection)
admin.site.register(Floor)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin, ExportAsCSV):
    list_display = ('name', 'floor', 'building_section')
    actions = ["export_as_csv"]


admin.site.register(DeviceCategory)
admin.site.register(DeviceManufacturer)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin, ExportAsCSV):
    list_display = ('name', 'room', 'device_category', 'device_manufacturer', 'status', 'purchase_data', 'serial_number')
    actions = ["export_as_csv"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin, ExportAsCSV):
    list_display = ('device', 'title', 'status', 'created_at', 'created_by')
    actions = ["export_as_csv"]


# admin.site.register(TicketComment)
