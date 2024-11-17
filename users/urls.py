from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('myaccount/', views.myAccount, name="myaccount"),
    path('register2/',views.register_view,name="register2"),
    path('login2/',views.login_view,name="login2"),

]