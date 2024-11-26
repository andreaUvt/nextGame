from django.shortcuts import render
from .models import Game
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    return render(request, 'home.html')

def games(request, category=None):
    page = request.GET.get('page', 1)  # Get the current page number from query params
    games_per_page = 20  # Number of games to display per page

    if category:  # If a category is specified, filter games by it
        games = Game.objects.filter(genres__icontains=category)  # Case-insensitive filter for the genre
    else:
        games = Game.objects.all()  # Fetch all games if no category is specified

    paginator = Paginator(games, games_per_page)  # Paginate games
    games_page = paginator.get_page(page)  # Get the requested page

    return render(request, 'games.html', {
        'games_page': games_page,
        'selected_category': category,  # Pass the selected category to the template
    })

def profile(request):
    return render(request, 'profile.html')
