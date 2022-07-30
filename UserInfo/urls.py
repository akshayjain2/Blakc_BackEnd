from django.contrib import admin
from django.urls import path
import views

urlpatterns = [

    path('signup/', views.createUser),
    path('login/',views.login),
    path('viewConsole',views.getTeams),
    path('getuser',views.userlist)
]