from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm


from collections import Counter

from nextGameApp.models import Game

# Create your views here.


def loginUser(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method=='POST':
        username=request.POST['username'].lower()
        password=request.POST['password']

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else '/')
        else:
            messages.error(request,'Username OR password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "You logged out!")
    return redirect('login')

def registerUser(request):

    if request.user.is_authenticated:
        return redirect('/')
    page='register'
    form=CustomUserCreationForm
    context={'page': page,'form': form}

    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.info(request, "Account created!")

            return redirect('login')
        else:
            for error in form.errors:
                messages.error(request, f'Error {error}')
                
            
    return render(request,'users/login_register.html',context)




@login_required(login_url='login')
def myAccount(request):
    user = request.user
    profile = user.profile

    context = {
        'username': profile.username,
    }
    return render(request, 'users/myaccount.html', context)