from django.urls import path, include
from accounts import views

#yemi
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register,dashboard, activation_view 

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('no_team', views.no_team, name='no_team'),
    path('create_team', views.create_team, name='create_team'),
    path('manage_teams', views.manage_teams, name='manage_teams'),
    path('teams/<int:team_id>', views.team, name='team'),
    path('teams/<int:team_id>/delete_team', views.delete_team, name='delete_team'),
    path('teams/<int:team_id>/update_team', views.update_team, name='update_team'),

    path('register/', register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/password_reset.html'
            ),
        name='password_reset'),
    path('password-reset/done',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
            ),
        name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html'
            ),
        name='password_reset_confirm'),

    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
            ),
        name='password_reset_complete'),
    path('accounts/activate/<activation_key>/', activation_view, name='activation_view' )
]