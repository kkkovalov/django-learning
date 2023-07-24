from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login-page"),
    path('logout/', views.logoutUser, name="logout-page"),
    path('register/', views.registerUser, name="register-page"),
    path('', views.home, name="home-page"),
    path('room/<str:pk>/', views.room, name="room-page"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>', views.deleteMessage, name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]
