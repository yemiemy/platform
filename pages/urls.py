from django.urls import path, include
from pages import views

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('notifications', views.notifications, name='notifications'),
]