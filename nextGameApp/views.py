from django.shortcuts import render, get_object_or_404, redirect
from .models import Game
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .game_recommender import recommend
# Create your views here.

def home(request):
    played_games_names = get_games_for_profile(request)

    recommended_games_names = recommend(played_games_names)
    
    recommended_games = Game.objects.filter(name__in=recommended_games_names)


    # Render the template with recommended games
    return render(request, 'home.html', {"recommended_games": recommended_games})


@login_required
def get_games_for_profile(request):
    # Get the logged-in user's profile
    profile = request.user.profile 
    
    # Retrieve all favorite and played games
    favorite_games_names = profile.favorite_games.values_list('name', flat=True)
    played_games_names = profile.played_games.values_list('name', flat=True)
    
    # Combine the names into a single list
    all_game_names = list(favorite_games_names) + list(played_games_names)
    
    # Optionally, remove duplicates (if any)
    all_game_names = list(set(all_game_names))
    
    return all_game_names


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

    games = games.order_by('-reviews_count')
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

@login_required
def add_to_favorites(request, game_id):
    from users.models import Profile
    from nextGameApp.models import Game
    game = get_object_or_404(Game, id=game_id)
    profile = request.user.profile
    profile.favorite_games.add(game)
    messages.success(request, f"{game.name} added to your favorites!")
    return redirect('game_detail', game_id=game_id)

@login_required
def add_to_to_play(request, game_id):
    from users.models import Profile
    from nextGameApp.models import Game
    game = get_object_or_404(Game, id=game_id)
    profile = request.user.profile
    profile.to_play_games.add(game)
    messages.success(request, f"{game.name} added to your to-play list!")
    return redirect('game_detail', game_id=game_id)

@login_required
def add_to_played(request, game_id):
    from users.models import Profile
    from nextGameApp.models import Game
    game = get_object_or_404(Game, id=game_id)
    profile = request.user.profile
    profile.played_games.add(game)
    messages.success(request, f"{game.name} added to your played games!")
    return redirect('game_detail', game_id=game_id)

@login_required
def favorite_games(request):
    profile = request.user.profile
    favorite_games = profile.favorite_games.all()
    return render(request, 'favorite_games.html', {'favorite_games': favorite_games})

@login_required
def favorite_games(request):
    profile = request.user.profile
    favorite_games = profile.favorite_games.all()  # Get the user's favorite games

    # Pagination
    paginator = Paginator(favorite_games, 10)  # Adjust the number of games per page as needed
    page_number = request.GET.get('page')
    games_page = paginator.get_page(page_number)

    context = {
        'games_page': games_page,
        'category_title': 'Favorites',
    }
    return render(request, 'games.html', context)

@login_required
def remove_from_favorites(request, game_id):
    profile = request.user.profile
    game = get_object_or_404(Game, id=game_id)
    if game in profile.favorite_games.all():
        profile.favorite_games.remove(game)
    return redirect('game_detail', game_id=game.id)

@login_required
def played_games(request):
    played_games_list = request.user.profile.played_games.all()
    return render(request, 'games.html', {'games_page': played_games_list})

@login_required
def add_to_played(request, game_id):
    profile = request.user.profile
    game = get_object_or_404(Game, id=game_id)
    if game not in profile.played_games.all():
        profile.played_games.add(game)
    return redirect('game_detail', game_id=game.id)

@login_required
def remove_from_played(request, game_id):
    profile = request.user.profile
    game = get_object_or_404(Game, id=game_id)
    if game in profile.played_games.all():
        profile.played_games.remove(game)
    return redirect('game_detail', game_id=game.id)

@login_required
def next_games(request):
    next_games_list = request.user.profile.to_play_games.all()
    return render(request, 'games.html', {'games_page': next_games_list})

@login_required
def add_to_next(request, game_id):
    profile = request.user.profile
    game = get_object_or_404(Game, id=game_id)
    if game not in profile.to_play_games.all():
        profile.to_play_games.add(game)
    return redirect('game_detail', game_id=game.id)

@login_required
def remove_from_next(request, game_id):
    profile = request.user.profile
    game = get_object_or_404(Game, id=game_id)
    if game in profile.to_play_games.all():
        profile.to_play_games.remove(game)
    return redirect('game_detail', game_id=game.id)