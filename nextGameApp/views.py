from django.shortcuts import render, get_object_or_404
from .models import Game
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request, 'home.html')

def games(request, category=None):
    page = request.GET.get('page', 1)  # Get the current page number from query params
    games_per_page = 20  # Number of games to display per page
    search_query = request.GET.get('search', '')  # Get the search query from query params

    if category:  # If a category is specified, filter games by it
        games = Game.objects.filter(genres__icontains=category)  # Case-insensitive filter for the genre
    else:
        games = Game.objects.all()  # Fetch all games if no category is specified

    if search_query:  # If a search query is provided, further filter the games
        games = games.filter(name__icontains=search_query)  # Case-insensitive filter for the game name

    paginator = Paginator(games, games_per_page)  # Paginate games
    games_page = paginator.get_page(page)  # Get the requested page

    return render(request, 'games.html', {
        'games_page': games_page,
        'selected_category': category,  # Pass the selected category to the template
        'search_query': search_query,  # Pass the search query to the template
    })


def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)  # Fetch the game or return 404 if not found
    return render(request, 'game.html', {'game': game})

def profile(request):
    return render(request, 'profile.html')
