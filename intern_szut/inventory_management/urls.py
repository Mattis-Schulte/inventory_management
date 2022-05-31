from django.urls import path, re_path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('overview/', views.overview, name='overview'),
    path('rooms/', views.rooms, name='rooms'),
    re_path(r'^rooms/(?P<room_name>.*)?/$', views.room_details, name='room_details'),
    path('devices/', views.devices, name='devices'),
    path('ticket-management/', views.ticket_management, name='ticket-management'),
    path('account/', views.account, name='account'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout, name='logout')
]
