from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return redirect('overview')

def overview(request):
    return render(request, 'overview.html')

def rooms(request):
    return render(request, 'rooms.html')

def devices(request):
    return render(request, 'devices.html')

def ticket_management(request):
    return render(request, 'ticket_management.html')

def page_not_found_view(request, exception):
    return redirect('overview')

def page_error(request):
    return redirect('overview')