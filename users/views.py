from django.shortcuts import render, redirect
from django.http import request
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from users.forms import CustomUserCreationForm
from .models import Profile
# Create your views here.

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('profiles')
        else:
            messages.error('Username OR password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(redirect)
    messages.info(request,'User logged out successfully!')
    return redirect('/login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.methods == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User account was created!')
            login(request, user)
            return redirect('profiles')
        else:
            messages.success(request,'An error has occured during registration')
    context={
        'page':page,
        'form':form
    }
    return render(request, 'users/login_register.html',context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request, 'users/profiles.html',context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile':profile,'topSkills':topSkills,'otherSkills':otherSkills}
    return render(request,'users/user-profile.html',context)
