from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.report_incident, name='report_incident'),
    path('request_help/', views.request_help, name='request_help'),
    path('start_chat/', views.start_chat, name='start_chat'),
    path('schedule_appointment/', views.schedule_appointment, name='schedule_appointment'),
    path('info/', views.view_information, name='view_information'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
