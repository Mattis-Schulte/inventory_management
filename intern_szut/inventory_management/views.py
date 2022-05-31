from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from inventory_management import verify_login
from datetime import date, timedelta
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.translation import gettext_lazy as _

from inventory_management.models import BuildingSection, Floor, Room, DeviceCategory, DeviceManufacturer, Device


def get_enum_choices(enum_data, append_unknown=False):
    unknown = {'id': 'unknown', 'label': _('Unbekannter Status')}
    enum_choices = []

    for status in enum_data:
        devices_statuses_dict = {'id': enum_data(status).value, 'label': enum_data(status).label}
        enum_choices.append(devices_statuses_dict)

    if append_unknown:
        enum_choices.append(unknown)

    return enum_choices


def make_labels_readable(enum_data, status_options, label_key: str):
    label_name = label_key + '_label'
    for data_set in enum_data:
        if data_set[label_key] is not None:
            data_set[label_name] = status_options(data_set[label_key]).label
        else:
            data_set[label_key] = 'unknown'
            data_set[label_name] = _('Unbekannt')

    return enum_data


def filter_devices_by_warranty(devices_data, filter_date=None, warranty_type=True):
    """ Filters devices by warranty date. """
    for device in devices_data:
        if device['purchase_data'] is not None and device['warranty_period_years'] is not None or device[ 'warranty_period_months'] is not None:
            if device['warranty_period_years'] is None:
                device['warranty_period_years'] = 0
            if device['warranty_period_months'] is None:
                device['warranty_period_months'] = 0
            warranty_expired_date = device['purchase_data'] + timedelta(days=device['warranty_period_years'] * 365.25) + timedelta(days=device['warranty_period_months'] * 30.437)
            if filter_date is not None and warranty_type:
                if not filter_date >= warranty_expired_date > date.today():
                    devices_data = devices_data.exclude(id=device['id'])
            elif filter_date is None and warranty_type:
                if warranty_expired_date < date.today():
                    devices_data = devices_data.exclude(id=device['id'])
            elif filter_date is None and not warranty_type:
                if not warranty_expired_date < date.today():
                    devices_data = devices_data.exclude(id=device['id'])
        else:
            devices_data = devices_data.exclude(id=device['id'])

    return devices_data


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

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'rooms.html', {'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data)})
    else:
        return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'rooms.html', 'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data)})


def room_details(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        room_data = Room.objects.filter(name=room_name).values('building_section__name', 'floor__name')[0]
        device_categories_data = DeviceCategory.objects.order_by('name').all().values('name', 'id')
        devices_data = Device.objects.filter(room__name=room_name).order_by('device_category__name', 'name').values('device_category__name', 'device_category__id', 'device_category__icon', 'name', 'status', 'id')
        devices_statuses_data = get_enum_choices(Device.StatusOptions, True)
        devices_data = make_labels_readable(devices_data, Device.StatusOptions, 'status')

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'room_details.html', {'room_name': room_name, 'room_data': room_data, 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data)})
        else:
            return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'room_details.html', 'room_name': room_name, 'room_data': room_data, 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data)})
    else:
        return redirect('rooms')


def devices(request):
    valid_filters = [
        {'name': 'status-filter', 'value': 'device-status-id-', 'result': 'status'},
        {'name': 'device-categories-filter', 'value': 'device-category-id-', 'result': 'device_category__id'},
        {'name': 'device-manufacture-filter', 'value': 'device-manufacture-id-', 'result': 'device_manufacturer__id'},
        {'name': 'device-price-filter', 'value': 'device-price-step-id-', 'result': 'price'},
        {'name': 'device-warranty-filter', 'value': 'device-warranty-step-id-',  'result': 'purchase_data'},
        {'name': 'device-purchase-date-filter', 'value': 'device-purchase-date-step-id-', 'result': 'purchase_data'}
    ]
    price_steps = [
        {'id': 0, 'label': _('Unter 100 €'), 'min_value': 100, 'max_value': 100},
        {'id': 1, 'label': _('100 – 300 €'), 'min_value': 100, 'max_value': 300},
        {'id': 2, 'label': _('300 – 500 €'), 'min_value': 100, 'max_value': 500},
        {'id': 3, 'label': _('500 – 1000 €'), 'min_value': 100, 'max_value': 1000},
        {'id': 4, 'label': _('1000 – 3000 €'), 'min_value': 100, 'max_value': 3000},
        {'id': 5, 'label': _('3000 – 5000 €'), 'min_value': 100, 'max_value': 5000},
        {'id': 6, 'label': _('Über 5000 €'), 'min_value': 100, 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekannter Preis'), 'max_value': None}
    ]
    remaining_warranty_steps = [
        {'id': 0, 'label': _('Unter 3 Monaten'), 'max_value': 3},
        {'id': 1, 'label': _('Unter 6 Monaten'), 'max_value': 6},
        {'id': 2, 'label': _('Unter 1 Jahr'), 'max_value': 12},
        {'id': 3, 'label': _('Unter 3 Jahre'), 'max_value': 36},
        {'id': 4, 'label': _('Unter 5 Jahre'), 'max_value': 60},
        {'id': 5, 'label': _('Unter 10 Jahre'), 'max_value': 120},
        {'id': 6, 'label': _('Jede restliche Garantie'), 'max_value': None},
        {'id': 7, 'label': _('Abgelaufene Garantie'), 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekannte Garantiezeit'), 'max_value': None}
    ]
    date_of_purchase_steps = [
        {'id': 0, 'label': _('Letzten 3 Monaten'), 'max_value': 3},
        {'id': 1, 'label': _('Letzten 6 Monaten'), 'max_value': 6},
        {'id': 2, 'label': _('Letztes 1 Jahr'), 'max_value': 12},
        {'id': 3, 'label': _('Letzten 3 Jahre'), 'max_value': 36},
        {'id': 4, 'label': _('Letzten 5 Jahre'), 'max_value': 60},
        {'id': 5, 'label': _('Letzten 10 Jahre'), 'max_value': 120},
        {'id': 6, 'label': _('Jedes Anschaffungsdatum'), 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekanntes Anschaffungsdatum'), 'max_value': None}
    ]

    device_categories_data = DeviceCategory.objects.order_by('name').all().values('name', 'id')
    devices_data = Device.objects.order_by('device_category__name', 'name').all().values('device_category__name', 'device_category__icon', 'room__name', 'price', 'device_manufacturer', 'purchase_data', 'warranty_period_years', 'warranty_period_months', 'name', 'status', 'id')
    devices_statuses_data = get_enum_choices(Device.StatusOptions, True)
    device_manufacturers_data = DeviceManufacturer.objects.order_by('name').all().values('name', 'id')

    for filter in valid_filters:
        request_data = request.GET.get(filter['name'])
        if request_data is not None:
            request_data = request.GET.get(filter['name']).replace(filter['value'], '')
            if request_data == 'unknown':
                if filter['name'] == 'device-warranty-filter':
                    devices_data = devices_data.filter(Q(purchase_data__isnull=True) | Q(warranty_period_years__isnull=True) & Q(warranty_period_months__isnull=True))
                else:
                    devices_data = devices_data.filter(**{filter['result'] + '__isnull': True})
            elif request_data.isdigit():
                if filter['name'] == 'device-price-filter':
                    if int(request_data) < len(price_steps):
                        devices_data = devices_data.filter(**{filter['result'] + '__lte': price_steps[int(request_data)]['max_value']})
                    else:
                        return redirect('devices')
                elif filter['name'] == 'device-warranty-filter':
                    if int(request_data) < len(remaining_warranty_steps):
                        if remaining_warranty_steps[int(request_data)]['max_value'] is not None:
                            filter_date = date.today() + timedelta(days=remaining_warranty_steps[int(request_data)]['max_value']) * 30.437
                            devices_data = filter_devices_by_warranty(devices_data, filter_date)
                        elif remaining_warranty_steps[int(request_data)]['id'] == 6:
                            devices_data = filter_devices_by_warranty(devices_data)
                        else:
                            devices_data = filter_devices_by_warranty(devices_data, None, False)
                    else:
                        return redirect('devices')
                elif filter['name'] == 'device-purchase-date-filter':
                    if int(request_data) < len(date_of_purchase_steps):
                        if date_of_purchase_steps[int(request_data)]['max_value'] is not None:
                            date_to_filter = date.today() - timedelta(days=date_of_purchase_steps[int(request_data)]['max_value']) * 30.437
                            devices_data = devices_data.filter(**{filter['result'] + '__gte': date_to_filter})
                        else:
                            pass
                    else:
                        return redirect('devices')
                elif filter['name'] == 'status-filter' and int(request_data) in [status['id'] for status in devices_statuses_data]:
                    devices_data = devices_data.filter(**{filter['result'] + '__exact': request_data})
                elif filter['name'] == 'device-categories-filter' and device_categories_data.filter(id=request_data).exists():
                    devices_data = devices_data.filter(**{filter['result'] + '__exact': request_data})
                elif filter['name'] == 'device-manufacture-filter' and device_manufacturers_data.filter(id=request_data).exists():
                    devices_data = devices_data.filter(**{filter['result'] + '__exact': request_data})
                else:
                    return redirect('devices')
            else:
                return redirect('devices')

    devices_data = make_labels_readable(devices_data, Device.StatusOptions, 'status')
    unique_devices_count = devices_data.count()
    unique_rooms_count = devices_data.values('room__name').distinct().count()
    unique_device_categories = devices_data.values('device_category__name').distinct().count()
    unique_device_manufacturers = devices_data.values('device_manufacturer__name').distinct().count()

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'devices.html', {'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': price_steps, 'remaining_warranty_steps': remaining_warranty_steps, 'date_of_purchase_steps': date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_rooms_count': unique_rooms_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers})
    else:
        return render(request, 'index.html', {'current_page_category': 'devices', 'current_page_file': 'devices.html', 'device_categories_data': list(device_categories_data), 'devices_statuses_data': list(devices_statuses_data), 'devices_data': list(devices_data), 'device_manufacturers_data': list(device_manufacturers_data), 'price_steps': price_steps, 'remaining_warranty_steps': remaining_warranty_steps, 'date_of_purchase_steps': date_of_purchase_steps, 'unique_devices_count': unique_devices_count, 'unique_rooms_count': unique_rooms_count, 'unique_device_categories': unique_device_categories, 'unique_device_manufacturers': unique_device_manufacturers})


def ticket_management(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'ticket-management.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'ticket-management', 'current_page_file': 'ticket-management.html'})


def account(request):
    if request.user.is_authenticated:
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
