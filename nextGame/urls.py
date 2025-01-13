"""
URL configuration for nextGame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from nextGameApp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('games/',views.games,name='games'),
    path('profile/',views.profile,name='profile',),
    path('games/<str:category>/', views.games, name='games_by_category'),  
    path('game/<int:game_id>/', views.game_detail, name='game_detail'), 
    path('',include('users.urls')),
    path('game/<int:game_id>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('game/<int:game_id>/add_to_to_play/', views.add_to_to_play, name='add_to_to_play'),
    path('game/<int:game_id>/add_to_played/', views.add_to_played, name='add_to_played'),
    path('favorites/', views.favorite_games, name='favorite_games'),
    path('game/<int:game_id>/remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('played/', views.played_games, name='played_games'),
    path('game/<int:game_id>/add_to_played/', views.add_to_played, name='add_to_played'),
    path('game/<int:game_id>/remove_from_played/', views.remove_from_played, name='remove_from_played'),
    path('next/', views.next_games, name='next_games'),
    path('game/<int:game_id>/add_to_next/', views.add_to_next, name='add_to_next'),
    path('game/<int:game_id>/remove_from_next/', views.remove_from_next, name='remove_from_next'),
    
]
