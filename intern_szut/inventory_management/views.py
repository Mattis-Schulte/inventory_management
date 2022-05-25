from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import verify_login


def index(request):
    return redirect('overview')

def overview(request):
    # If request is ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'overview.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'overview', 'current_page_file': 'overview.html'})

def rooms(request):
    # If request is ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'rooms.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'rooms', 'current_page_file': 'rooms.html'})

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
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'account.html')
    else:
        return render(request, 'index.html', {'current_page_category': 'account', 'current_page_file': 'account.html'})

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
                            response = HttpResponse(f'User data: {user_data}, User role: {user_role}')
                            return response

                return HttpResponse(f'Error on: {error_on}, HTTP-Code: {http_code}, Error-Code: {error_message}')
            return HttpResponse('Username or password is too long')
        return HttpResponse('Username or password is missing')

def page_not_found_view(request, exception):
    # If request is ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(status=404)
    else:
        return redirect('overview')

def page_error(request):
    # If request is ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponse(status=500)
    else:
        return redirect('overview')