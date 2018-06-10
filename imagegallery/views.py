from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from imagegallery.models import UserProfile
from django.db import IntegrityError


def login_user(request):
    """
    Takes care of logging users in with Django's own login functionalities.
    """
    logout(request)
    username = password = ''
    if request.POST:
 
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(user)
        print(username, password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')

    print("Login failed!")    
    return render(request, 'imagegallery/login.html')


def edit_profile(request):
    return redirect('/')


def signup_user(request):
    """
    Creates a new user to the database, using UserProfile model and the form found in
    templates/webstore/signup.html.
    """
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return render(request, 'imagegallery/signup.html',
                          {"message": "Username '" +
                           username + "' is already taken"})
        user.is_active = True
        user.save()
        
        profile = UserProfile.objects.create(user=user)

        if request.POST.get('admin', False):
            profile.is_admin = True
        else:
            profile.is_admin = False
        profile.save()
        print("created user with",username,password)
        return redirect('/')
    
    return render(request, 'imagegallery/signup.html')


@login_required(login_url='/login')
def logout_user(request):
    """
    Logs the user out with Django's default logout functionality.
    """
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')

