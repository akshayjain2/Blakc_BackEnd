from django.urls import path
from Team import views

urlpatterns = [
    path('createTeam',views.createTeam),
    path('AddTeamMember',views.addMember),
    path('viewAccessofTeammember',views.viewAcess),
    path('DeleteTeam',views.deleteTeam),
    path('ModifyTeamMember',views.modifyteammember),
    path('removeTeamMember',views.removeTeamMember),
]