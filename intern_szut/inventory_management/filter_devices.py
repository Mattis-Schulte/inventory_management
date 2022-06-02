from django.db.models import Q
from datetime import date, timedelta
from django.utils.translation import gettext_lazy as _


class FilterDevices:
    valid_filters = [
        {'name': 'status-filter', 'value': 'device-status-id-', 'result': 'status'},
        {'name': 'device-categories-filter', 'value': 'device-category-id-', 'result': 'device_category__id'},
        {'name': 'device-manufacture-filter', 'value': 'device-manufacture-id-', 'result': 'device_manufacturer__id'},
        {'name': 'device-price-filter', 'value': 'device-price-step-id-', 'result': 'price'},
        {'name': 'device-warranty-filter', 'value': 'device-warranty-step-id-',  'result': 'purchase_data'},
        {'name': 'device-purchase-date-filter', 'value': 'device-purchase-date-step-id-', 'result': 'purchase_data'}
    ]
    price_steps = [
        {'id': 0, 'label': _('Unter 100 €'), 'min_value': 0, 'max_value': 100},
        {'id': 1, 'label': _('100 – 300 €'), 'min_value': 100, 'max_value': 300},
        {'id': 2, 'label': _('300 – 500 €'), 'min_value': 300, 'max_value': 500},
        {'id': 3, 'label': _('500 – 1.000 €'), 'min_value': 500, 'max_value': 1000},
        {'id': 4, 'label': _('1.000 – 3.000 €'), 'min_value': 1000, 'max_value': 3000},
        {'id': 5, 'label': _('3.000 – 5.000 €'), 'min_value': 3000, 'max_value': 5000},
        {'id': 6, 'label': _('5.000 – 10.000 €'), 'min_value': 5000, 'max_value': 10000},
        {'id': 7, 'label': _('Über 10.000 €'), 'min_value': 10000, 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekannter Preis'), 'max_value': None}
    ]
    remaining_warranty_steps = [
        {'id': 0, 'label': _('Unter 3 Monaten'), 'max_value': 3},
        {'id': 1, 'label': _('Unter 6 Monaten'), 'max_value': 6},
        {'id': 2, 'label': _('Unter 1 Jahr'), 'max_value': 12},
        {'id': 3, 'label': _('Unter 3 Jahre'), 'max_value': 36},
        {'id': 4, 'label': _('Unter 5 Jahre'), 'max_value': 60},
        {'id': 5, 'label': _('Unter 10 Jahre'), 'max_value': 120},
        {'id': 6, 'label': _('Jede gültige Garantie'), 'max_value': None},
        {'id': 7, 'label': _('Abgelaufene Garantie'), 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekannte Garantiezeit'), 'max_value': None}
    ]
    date_of_purchase_steps = [
        {'id': 0, 'label': _('Letzten 3 Monaten'), 'max_value': 3},
        {'id': 1, 'label': _('Letzten 6 Monaten'), 'max_value': 6},
        {'id': 2, 'label': _('Letztes Jahr'), 'max_value': 12},
        {'id': 3, 'label': _('Letzten 3 Jahre'), 'max_value': 36},
        {'id': 4, 'label': _('Letzten 5 Jahre'), 'max_value': 60},
        {'id': 5, 'label': _('Letzten 10 Jahre'), 'max_value': 120},
        {'id': 6, 'label': _('Jedes Anschaffungsdatum'), 'max_value': None},
        {'id': 'unknown', 'label': _('Unbekanntes Anschaffungsdatum'), 'max_value': None}
    ]

    @classmethod
    def filter_devices_by_warranty(cls, devices_data, filter_date=None, warranty_type=True):
        for device in devices_data:
            if device['purchase_data'] is not None and device['warranty_period_years'] is not None or device['warranty_period_months'] is not None:
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

    @classmethod
    def filter_devices_main(cls, devices_data, get_parameters, devices_statuses_data, device_categories_data, device_manufacturers_data):
        number_of_filters_applied = 0

        for _filter in cls.valid_filters:
            request_data = get_parameters.get(_filter['name'])
            if request_data is not None:
                number_of_filters_applied += 1
                request_data = request_data.replace(_filter['value'], '')
                if request_data == 'unknown' and _filter['name'] != 'device-categories-filter':
                    if _filter['name'] == 'device-warranty-filter':
                        devices_data = devices_data.filter(Q(purchase_data__isnull=True) | Q(warranty_period_years__isnull=True) & Q(warranty_period_months__isnull=True))
                    else:
                        devices_data = devices_data.filter(**{_filter['result'] + '__isnull': True})
                elif request_data.isdigit():
                    if _filter['name'] == 'device-price-filter':
                        if int(request_data) < len(cls.price_steps):
                            if cls.price_steps[int(request_data)]['max_value'] is not None:
                                devices_data = devices_data.filter(**{_filter['result'] + '__gte': cls.price_steps[int(request_data)]['min_value'], _filter['result'] + '__lte': cls.price_steps[int(request_data)]['max_value']})
                            else:
                                devices_data = devices_data.filter(**{_filter['result'] + '__gte': cls.price_steps[int(request_data)]['min_value']})
                        else:
                            return None, number_of_filters_applied
                    elif _filter['name'] == 'device-warranty-filter':
                        if int(request_data) < len(cls.remaining_warranty_steps):
                            if cls.remaining_warranty_steps[int(request_data)]['max_value'] is not None:
                                filter_date = date.today() + timedelta(days=cls.remaining_warranty_steps[int(request_data)]['max_value']) * 30.437
                                devices_data = cls.filter_devices_by_warranty(devices_data, filter_date)
                            elif cls.remaining_warranty_steps[int(request_data)]['id'] == 6:
                                devices_data = cls.filter_devices_by_warranty(devices_data)
                            else:
                                devices_data = cls.filter_devices_by_warranty(devices_data, None, False)
                        else:
                            return None, number_of_filters_applied
                    elif _filter['name'] == 'device-purchase-date-filter':
                        if int(request_data) < len(cls.date_of_purchase_steps):
                            if cls.date_of_purchase_steps[int(request_data)]['max_value'] is not None:
                                date_to_filter = date.today() - timedelta(days=cls.date_of_purchase_steps[int(request_data)]['max_value']) * 30.437
                                devices_data = devices_data.filter(**{_filter['result'] + '__gte': date_to_filter})
                            else:
                                pass
                        else:
                            return None, number_of_filters_applied
                    elif _filter['name'] == 'status-filter' and int(request_data) in [status['id'] for status in devices_statuses_data]:
                        devices_data = devices_data.filter(**{_filter['result'] + '__exact': request_data})
                    elif _filter['name'] == 'device-categories-filter' and device_categories_data.filter(id=request_data).exists():
                        devices_data = devices_data.filter(**{_filter['result'] + '__exact': request_data})
                    elif _filter['name'] == 'device-manufacture-filter' and device_manufacturers_data.filter(id=request_data).exists():
                        devices_data = devices_data.filter(**{_filter['result'] + '__exact': request_data})
                    else:
                        return None, number_of_filters_applied
                else:
                    return None, number_of_filters_applied

        return devices_data, number_of_filters_applied
