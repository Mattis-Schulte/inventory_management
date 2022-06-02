from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from inventory_management import filter_rooms, filter_devices, verify_login, get_choices
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from inventory_management.models import BuildingSection, Floor, Room, DeviceCategory, DeviceManufacturer, Device, Ticket, TicketComment


def search(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse('Search')
    else:
        return redirect('overview')


def overview(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'overview.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'overview', 'current_page_file': 'overview.html'})


def rooms(request):
    building_section_data = BuildingSection.objects.order_by('name').all().values('name', 'id')
    floor_data = Floor.objects.order_by('name').all().values('name', 'id')
    room_data = Room.objects.order_by('name').all().values('building_section__name', 'building_section__id', 'floor__name', 'floor__id', 'name')

    room_data_temp, number_of_filters_applied = filter_rooms.FilterRooms.filter_devices_main(room_data, request.GET, floor_data, building_section_data)
    if room_data_temp is None:
        return redirect('rooms')
    else:
        room_data = room_data_temp

    unique_rooms_count = room_data.count()
    unique_floors_count = room_data.values('floor__id').distinct().count()
    unique_building_sections_count = room_data.values('building_section__id').distinct().count()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'rooms.html', {'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data), 'unique_rooms_count': unique_rooms_count, 'unique_floors_count': unique_floors_count, 'unique_building_sections_count': unique_building_sections_count, 'number_of_filters_applied': number_of_filters_applied})
    else:
        return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'rooms.html', 'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data), 'unique_rooms_count': unique_rooms_count, 'unique_floors_count': unique_floors_count, 'unique_building_sections_count': unique_building_sections_count, 'number_of_filters_applied': number_of_filters_applied})


def room_details(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        room_data = Room.objects.filter(name=room_name).values('building_section__name', 'floor__name', 'name')[0]
        device_categories_data = DeviceCategory.objects.order_by('name').all().values('name', 'id')
        devices_data = Device.objects.filter(room__name=room_name).order_by('device_category__name', 'name').values('device_category__name', 'device_category__icon', 'room__name', 'price', 'device_manufacturer', 'purchase_data', 'warranty_period_years', 'warranty_period_months', 'name', 'status', 'id')
        devices_statuses_data = get_choices.GetChoices.get_enum_choices(Device.StatusOptions, True)
        device_manufacturers_data = DeviceManufacturer.objects.order_by('name').all().values('name', 'id')

        devices_data_temp, number_of_filters_applied = filter_devices.FilterDevices.filter_devices_main(devices_data, request.GET, devices_statuses_data, device_categories_data, device_manufacturers_data)
        if devices_data_temp is None:
            return redirect('room_details', room_name=room_name)
        else:
            devices_data = devices_data_temp

        devices_data = get_choices.GetChoices.make_labels_readable(devices_data, Device.StatusOptions, 'status')
        unique_devices_count = devices_data.count()
        unique_device_categories = devices_data.values('device_category__id').distinct().count()
        unique_device_manufacturers = devices_data.values('device_manufacturer__id').distinct().count()

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'room_details.html', {'room_data': room_data, 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': filter_devices.FilterDevices.price_steps, 'remaining_warranty_steps': filter_devices.FilterDevices.remaining_warranty_steps, 'date_of_purchase_steps': filter_devices.FilterDevices.date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers, 'number_of_filters_applied': number_of_filters_applied})
        else:
            return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'room_details.html', 'room_data': room_data, 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': filter_devices.FilterDevices.price_steps, 'remaining_warranty_steps': filter_devices.FilterDevices.remaining_warranty_steps, 'date_of_purchase_steps': filter_devices.FilterDevices.date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers, 'number_of_filters_applied': number_of_filters_applied})

    else:
        return redirect('rooms')


def devices(request):
    device_categories_data = DeviceCategory.objects.order_by('name').all().values('name', 'id')
    devices_data = Device.objects.order_by('device_category__name', 'name').all().values('device_category__name', 'device_category__icon', 'room__name', 'price', 'device_manufacturer', 'purchase_data', 'warranty_period_years', 'warranty_period_months', 'name', 'status', 'id')
    devices_statuses_data = get_choices.GetChoices.get_enum_choices(Device.StatusOptions, True)
    device_manufacturers_data = DeviceManufacturer.objects.order_by('name').all().values('name', 'id')

    devices_data_temp, number_of_filters_applied = filter_devices.FilterDevices.filter_devices_main(devices_data, request.GET, devices_statuses_data, device_categories_data, device_manufacturers_data)
    if devices_data_temp is None:
        return redirect('devices')
    else:
        devices_data = devices_data_temp

    devices_data = get_choices.GetChoices.make_labels_readable(devices_data, Device.StatusOptions, 'status')
    unique_devices_count = devices_data.count()
    unique_rooms_count = devices_data.values('room__id').distinct().count()
    unique_device_categories = devices_data.values('device_category__id').distinct().count()
    unique_device_manufacturers = devices_data.values('device_manufacturer__id').distinct().count()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'devices.html', {'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': filter_devices.FilterDevices.price_steps, 'remaining_warranty_steps': filter_devices.FilterDevices.remaining_warranty_steps, 'date_of_purchase_steps': filter_devices.FilterDevices.date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_rooms_count': unique_rooms_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers, 'number_of_filters_applied': number_of_filters_applied})
    else:
        return render(request, 'index.html', {'current_page_category': 'devices', 'current_page_file': 'devices.html', 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': filter_devices.FilterDevices.price_steps, 'remaining_warranty_steps': filter_devices.FilterDevices.remaining_warranty_steps, 'date_of_purchase_steps': filter_devices.FilterDevices.date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_rooms_count': unique_rooms_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers, 'number_of_filters_applied': number_of_filters_applied})


def device_details(request, device_id):
    if Device.objects.filter(id=device_id).exists():
        device_data = Device.objects.filter(id=device_id).values('device_category__name', 'device_category__icon', 'room__name', 'price', 'device_manufacturer__name', 'purchase_data', 'warranty_period_years', 'warranty_period_months', 'serial_number', 'name', 'description', 'status')
        device_data = get_choices.GetChoices.make_labels_readable(device_data, Device.StatusOptions, 'status')[0]

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'device_details.html', {'device_data': device_data})
        else:
            return render(request, 'index.html', {'current_page_category': 'devices', 'current_page_file': 'device_details.html', 'device_data': device_data})
    else:
        return redirect('devices')


def ticket_management(request):
    tickets_data = Ticket.objects.order_by('last_change_at').all().values('id', 'title', 'description', 'status', 'created_at', 'created_by__first_name', 'created_by__last_name', 'last_change_at')
    tickets_statuses_data = get_choices.GetChoices.get_enum_choices(Ticket.StatusOptions)
    tickets_comments = TicketComment.objects.order_by('created_by').all().values('id', 'ticket__id', 'ticket__title', 'created_at', 'created_by__first_name', 'created_by__last_name', 'comment')

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'ticket-management.html', {'tickets_data': list(tickets_data), 'tickets_statuses_data': list(tickets_statuses_data), 'tickets_comments': list(tickets_comments)})
    else:
        return render(request, 'index.html', {'current_page_category': 'ticket-management', 'current_page_file': 'ticket-management.html', 'tickets_data': list(tickets_data), 'tickets_statuses_data': list(tickets_statuses_data), 'tickets_comments': list(tickets_comments)})


def account(request):
    if request.user.is_authenticated:
        print(request.user.has_perm('inventory_management.add_ticket'))
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'account.html')
        else:
            return render(request, 'index.html', {'current_page_category': 'account', 'current_page_file': 'account.html'})
    else:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return HttpResponse(status=401)
        else:
            return redirect('overview')


@csrf_protect
def login(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.POST['username'] and request.POST['password']:
            if len(request.POST['username']) < 50 and len(request.POST['password']) < 50:
                error_on = 'access_token'
                http_code, error_message, access_token = verify_login.VerifyLogin.get_access_token(request.POST['username'], request.POST['password'])
                if access_token:
                    error_on = 'user_data'
                    http_code, error_message, user_data = verify_login.VerifyLogin.get_user_data(access_token)
                    if user_data:
                        error_on = 'user_role'
                        http_code, error_message, user_role = verify_login.VerifyLogin.get_user_role(access_token)
                        if user_role:
                            user = authenticate(request, username=request.POST['username'], password=request.POST['password'], user_data=user_data, user_role=user_role)

                            if user is None:
                                response = HttpResponse('Unknown error, probably disabled account')
                            else:
                                auth_login(request, user)
                                response = HttpResponse(f'Success')

                            return response

                return HttpResponse(f'Error on: {error_on}, HTTP-Code: {http_code}, Error-Code: {error_message}')
            return HttpResponse('Username or password is too long')
        return HttpResponse('Username or password is missing')


def logout(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        auth_logout(request)
        return HttpResponse(f'Success')
    else:
        auth_logout(request)
        return redirect('overview')


def page_not_found_view(request, exception):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(status=404)
    else:
        return redirect('overview')


def page_error(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(status=500)
    else:
        return redirect('overview')
