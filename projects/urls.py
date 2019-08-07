from django.contrib import admin
from django.urls import path, include
from projects import views

urlpatterns = [
    path('create', views.create, name='create_project' ),
    path('', views.projects, name='projects' ),
    path('<int:project_id>', views.project, name='project' ),
    path('<int:project_id>/assign_project', views.assign_project, name='assign_project' ),
    path('<int:project_id>/submit_project', views.submit_project, name='submit_project' ),
    path('<int:project_id>/confirm_project', views.confirm_project, name='confirm_project' ),
    path('<int:project_id>/delete_project', views.delete_project, name='delete_project' ),
    path('<int:project_id>/update_project', views.update_project, name='update_project' ),
    path('issues', views.issues, name='issues'),
    path('<int:project_id>/create_issue', views.create_issue, name='create_issue' ),
    path('issue/<int:issue_id>', views.issue, name='issue' ),
    path('s/', views.search, name='search'),
    path('team/<int:team_id>', views.team_projects, name='team_projects'),
    path('<int:project_id>/solution', views.solution, name='solution'),
    path('<int:team_id>/feedback',views.create_feedback, name='create_feedback'),
    path('feedback/<int:feedback_id>',views.feedback, name='feedback'),
]