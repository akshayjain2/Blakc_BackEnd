from django.urls import path
from ChatApplication import views

urlpatterns = [

    path('sendChat/', views.sendChat),
    path('viewChats',views.viewChat),
    path('/api/v1/users',views.UserView),
    path('/api/v1/sessions',views.SessionView),
    path('/api/v1/posts',views.PostListView),
    path('/api/v1/posts/<int:id>',views.PostView),
    path('/api/v1/todos',views.ToDoListView),
    path('/api/v1/todos/<int:id>',views.ToDoView),
    path('/api/v1/contacts',views.ContactListView),
    path('/api/v1/contacts/<int:id>',views.ContactView),
    path('/api/v1/projects',views.ProjectListView),
    path('/api/v1/projects/<int:id>',views.ProjectView),
    path('/api/v1/issues',views.IssueListView),
    path('/api/v1/issues/<int:id>',views.IssueView),
    path('/api/v1/tags',views.TagListView),
    path('/api/v1/tags/<int:id>',views.TagView),
    path('/api/v1/milestones',views.MilestoneListView),
    path('/api/v1/milestones/<int:id>',views.MilestoneView),
    path('/api/v1/efforts',views.EffortListView),
    path('/api/v1/efforts/<int:id>',views.EffortView),
    path('/api/v1/columns',views.ColumnListView),
    path('/api/v1/columns/<int:id>',views.ColumnView),
]