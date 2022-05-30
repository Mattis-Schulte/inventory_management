from django.contrib import admin
from inventory_management.models import MyUser, BuildingSection, Floor, Room, DeviceCategory, DeviceManufacturer, Device, Ticket, TicketComment

class TicketAdmin(admin.ModelAdmin):
    list_display = ('device', 'title', 'description', 'status', 'created_at', 'created_by')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TicketAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        form.base_fields['created_by'].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'comment', 'created_at', 'created_by')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(TicketCommentAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['created_by'].initial = request.user
        form.base_fields['created_by'].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


# Register your models here.
admin.site.register(MyUser)
admin.site.register(BuildingSection)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(DeviceCategory)
admin.site.register(DeviceManufacturer)
admin.site.register(Device)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)