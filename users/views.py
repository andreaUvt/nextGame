from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm


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
    
    form = UserCreationForm()
    page='register'
    context={'page': page,'form': form,}
                
            
    return render(request,'users/login_register.html',context)



@login_required(login_url='login')
def myAccount(request):
    user = request.user
    profile = user.profile

    context = {
        'username': profile.username,
    }
    return render(request, 'users/myaccount.html', context)