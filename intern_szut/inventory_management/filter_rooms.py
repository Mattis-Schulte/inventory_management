class FilterRooms:
    valid_filters = [
        {'name': 'floor-filter', 'value': 'floor-id-', 'result': 'floor__id'},
        {'name': 'building-section-filter', 'value': 'building-section-id-', 'result': 'building_section__id'},
    ]

    @classmethod
    def filter_devices_main(cls, room_data, get_parameters, floor_data, building_section_data):
        number_of_filters_applied = 0

        for _filter in cls.valid_filters:
            request_data = get_parameters.get(_filter['name'])
            if request_data is not None:
                request_data = request_data.replace(_filter['value'], '')
                if request_data.isdigit():
                    number_of_filters_applied += 1
                    if _filter['name'] == 'floor-filter' and floor_data.filter(id=request_data).exists():
                        room_data = room_data.filter(**{_filter['result']: request_data})
                    elif _filter['name'] == 'building-section-filter' and building_section_data.filter(
                            id=request_data).exists():
                        room_data = room_data.filter(**{_filter['result']: request_data})
                    else:
                        return None, number_of_filters_applied
                else:
                    return None, number_of_filters_applied

        return room_data, number_of_filters_applied
