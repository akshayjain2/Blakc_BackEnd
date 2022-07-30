from django.urls import path
import views

urlpatterns = [

    path('sendChat/', views.sendChat),
    path('viewChats',views.viewChat),
]