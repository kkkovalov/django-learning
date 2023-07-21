from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home-page"),
    path('room/<str:pk>/', views.room, name="room-page"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
]
