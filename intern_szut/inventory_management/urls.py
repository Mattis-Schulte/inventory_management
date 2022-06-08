from django.urls import path, re_path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('overview/', views.overview, name='overview'),
    path('rooms/', views.rooms, name='rooms'),
    re_path(r'^rooms/(?P<room_name>.*)?/$', views.room_details, name='room-details'),
    path('devices/', views.devices, name='devices'),
    re_path(r'^devices/device-(?P<device_id>.*)?/$', views.device_details, name='device-details'),
    path('ticket-management/', views.ticket_management, name='ticket-management'),
    path('ticket-management/create-new-ticket/', views.create_new_ticket, name='create-new-ticket'),
    path('ticket-management/create-new-ticket/submit-new-ticket/', views.submit_new_ticket, name='submit-new-ticket'),
    re_path(r'^ticket-management/ticket-(?P<ticket_id>.*)?/$', views.ticket_details, name='ticket-details'),
    path('account/', views.account, name='account'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout, name='logout')
]
