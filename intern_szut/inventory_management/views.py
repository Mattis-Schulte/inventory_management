from django.shortcuts import render, redirect
from django.http import HttpResponse


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