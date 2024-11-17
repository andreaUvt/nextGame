from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def games(request):
    return render(request, 'games.html')

def profile(request):
    return render(request, 'profile.html')