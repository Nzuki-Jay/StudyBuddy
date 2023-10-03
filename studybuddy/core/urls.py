from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_user, name="login"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
    path('<int:pk>/', views.room, name="room"),
    path('delete-message/', views.delete_message, name="delete-message"),
    path('create-room/', views.create_room, name="create-room"),
    path('profile<int:pk>/', views.profile, name="profile"),
    path('update-room/<int:pk>/', views.update_room, name="update-room"),
    path('delete-room/', views.delete_room, name="delete-room"),
    path('update-profile/', views.update_profile, name="update-profile"),
    path('reply<int:pk>/', views.reply_message, name="reply-message")
]
