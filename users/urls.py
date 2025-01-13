from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('myaccount/', views.myAccount, name="myaccount"),
    path('game_history/', views.gameHistory, name="game_history"),
]