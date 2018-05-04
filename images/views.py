from django.shortcuts import render, redirect, HttpResponse
from images.models import Image, Album
from imagegallery.models import UserProfile
from hashlib import md5
import os
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from images.forms import ImageForm, AlbumForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


def view_album(request, name):
    print(name)

    try:
        album = Album.objects.get(name=name)
    except:
        return redirect('/')

    images = album.images.all()
    context = {'images': images}
    return render(request, 'album.html', context)


def add_image(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user.id 
            image.pic = request.FILES['pic']
            image.save()
	    
            album = Album.objects.get(pk=request['album'])
            album.images.add(image)
            album.save()

    else:
        form = ImageForm()

    return render(request, 'add_image.html', {'form': form})


def add_album(request):
    
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        
        if form.is_valid():
            album = form.save(commit=False)
            user = request.user
            profile = UserProfile.objects.get(user=user)
            album.creator = profile.id
            album.save()
            return redirect('/')

    else:
        form = AlbumForm()

    return render(request, 'add_album.html', {'form': form})
 
