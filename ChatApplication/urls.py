from django.urls import path
from ChatApplication import views

urlpatterns = [

    path('sendChat/', views.sendChat),
    path('viewChats',views.viewChat),
]