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
        return render(request, 'index.html', {'current_page': 'overview', 'current_page_file': 'overview.html'})

def rooms(request):
    # If request is ajax
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'rooms.html')
    else:
        return render(request, 'index.html', {'current_page': 'rooms', 'current_page_file': 'rooms.html'})

def devices(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'devices.html')
    else:
        return render(request, 'index.html', {'current_page': 'devices', 'current_page_file': 'devices.html'})

def ticket_management(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'ticket_management.html')
    else:
        return render(request, 'index.html', {'current_page': 'ticket_management', 'current_page_file': 'ticket_management.html'})

def account(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        access_token = verify_login.VerifyLogin.get_access_token(request.POST['username'], request.POST['password'])
        if access_token:
            user_role = verify_login.VerifyLogin.get_user_role(access_token)
            user_data = verify_login.VerifyLogin.get_user_data(access_token)
            response = HttpResponse(f'User data: {user_data}, User role: {user_role}')
            return response
        else:
            return HttpResponse('{"ErrorCode":"InvalidUser"}')
    elif request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return render(request, 'account.html')
    else:
        return render(request, 'index.html', {'current_page': 'account', 'current_page_file': 'account.html'})

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