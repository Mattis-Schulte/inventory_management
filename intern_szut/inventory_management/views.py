from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from inventory_management import verify_login
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from inventory_management.models import BuildingSection, Floor, Room


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
    room_data = Room.objects.order_by('building_section__name', 'floor__name', 'name').all().values('building_section__name', 'building_section__id', 'floor__name', 'floor__id', 'name')

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'rooms.html', {'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data)})
    else:
        return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'rooms.html', 'building_sections': list(building_section_data), 'floors': list(floor_data), 'rooms': list(room_data)})


def room_details(request, room_name):
    if Room.objects.filter(name=room_name).exists():
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return render(request, 'room_details.html', {'room_name': room_name})
        else:
            return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'room_details.html', 'room_name': room_name})
    else:
        return redirect('rooms')


def devices(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'devices.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'devices', 'current_page_file': 'devices.html'})


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
