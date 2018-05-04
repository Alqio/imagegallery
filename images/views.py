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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def create_pagination(request, items_all):
    nof_items_per_page = 6

    p = Paginator(items_all, nof_items_per_page)
    page = request.GET.get('page')

    try:
        items = p.page(page)
        page = int(page)
    except PageNotAnInteger:
        items = p.page(1)
        page = 1
    except EmptyPage:
        items = p.page(p.num_pages)
        page = p.num_pages

    context = {
        'items': items,
        'pages': p.page_range,
        'current_page': page,
        'amount': items_all.count(),
        'search_term': '?'
    }

    return context

def index(request):
    return HttpResponse("moi")


def albums(request):

    albums_all = Album.objects.all()

    print(albums_all)

    context = create_pagination(request, albums_all)
    return render(request, 'albums.html', context)


def view_album(request, id):

    try:
        album = Album.objects.get(pk=id)
    except:
        return redirect('/')

    images_all = album.images.all()
    context = create_pagination(request, images_all)
    context.update({'album': album})
    return render(request, 'album.html', context)


def view_image(request, id, album_id):
    
    try:
        image = Image.objects.get(pk=id)
    except:
        return redirect('/')

    context = {
        'image': image,
    }

    return render(request, 'image.html', context)


def add_image(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user.id

            try:
                image.pic = request.FILES['pic']
            except:
                messages.info(request, 'Kuvalle ei annettu kuvaa, käytetään oletusta.')
                print("No pic provided, using default image.")
            
            image.save()

            album = Album.objects.get(pk=request.POST['album'])
            album.images.add(image)
            album.save()
            form = ImageForm()

            messages.success(request, 'Kuva ladattiin onnistuneesti!')

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
            messages.success(request, 'Albumi ladattiin onnistuneesti!')
            return redirect('/')

    else:
        form = AlbumForm()

    return render(request, 'add_album.html', {'form': form})
 
