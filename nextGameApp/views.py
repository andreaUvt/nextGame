from django.shortcuts import render
from .models import Game
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request, 'home.html')

def games(request):
    page = request.GET.get('page', 1)  # Get the current page number from query params
    games_per_page = 20  # Number of games to display per page
    games = Game.objects.all()  # Fetch all games

    paginator = Paginator(games, games_per_page)  # Paginate games
    games_page = paginator.get_page(page)  # Get the requested page

    return render(request, 'games.html', {'games_page': games_page})
def profile(request):
    return render(request, 'profile.html')