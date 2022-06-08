from django.db.models import Q


class SearchData:
    @classmethod
    def search_tickets(cls, search_request, data_to_search):
        search_request_keywords = search_request.split(' ')
        search_request_keywords = filter(str.strip, search_request_keywords)
        tickets_data = []
        for keyword in search_request_keywords:
            current_keyword_query = data_to_search.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(device__name__icontains=keyword) | Q(device__device_manufacturer__name__icontains=keyword) | Q(created_by__first_name__icontains=keyword) | Q(created_by__last_name__icontains=keyword) | Q(device__room__name__icontains=keyword) | Q(device__device_category__name__icontains=keyword)).order_by('-last_change_at').all()
            if current_keyword_query and not any(ticket in tickets_data for ticket in current_keyword_query):
                tickets_data += current_keyword_query

        return tickets_data[:3]

    @classmethod
    def search_devices(cls, search_request, data_to_search):
        search_request_keywords = search_request.split(' ')
        search_request_keywords = filter(str.strip, search_request_keywords)
        devices_data = []
        for keyword in search_request_keywords:
            current_keyword_query = data_to_search.filter(Q(device_category__name__icontains=keyword) | Q(room__name__icontains=keyword) | Q(name__icontains=keyword) | Q(device_manufacturer__name__icontains=keyword) | Q(serial_number__icontains=keyword) | Q(description__icontains=keyword)).order_by('device_category__name', 'name').all()
            if current_keyword_query and not any(device in devices_data for device in current_keyword_query):
                devices_data += current_keyword_query

        return devices_data[:5]

    @classmethod
    def search_rooms(cls, search_request, data_to_search):
        search_request_keywords = search_request.split(' ')
        search_request_keywords = filter(str.strip, search_request_keywords)
        room_data = []
        for keyword in search_request_keywords:
            current_keyword_query = data_to_search.filter(Q(building_section__name__icontains=keyword) | Q(floor__name__icontains=keyword) | Q(name__icontains=keyword)).order_by('name').all()
            if current_keyword_query and not any(room in room_data for room in current_keyword_query):
                room_data += current_keyword_query

        return room_data[:5]
