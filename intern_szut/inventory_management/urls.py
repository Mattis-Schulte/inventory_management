from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('overview/', views.overview, name='overview'),
    path('rooms/', views.rooms, name='rooms'),
    path('devices/', views.devices, name='devices'),
    path('ticket-management/', views.ticket_management, name='ticket-management')
]
