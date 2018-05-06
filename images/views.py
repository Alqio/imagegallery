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
from django.db.models import Q

def create_pagination(request, items_all, item_name='items'):
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
        item_name: items,
        'pages': p.page_range,
        'current_page': page,
        'amount': items_all.count(),
        'search_term': '?'
    }

    return context


def index(request):
    return redirect('albums')


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


def view_image(request, id, album_id=1):
    
    try:
        image = Image.objects.get(pk=id)
    except:
        return redirect('/')
   
    try:
        uploader = UserProfile.objects.get(pk=image.uploader).user.username
    except:
        uploader = "Tuntematon"
    context = {
        'image': image,
        'uploader':uploader
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
            messages.success(request, 'Albumi luotiin onnistuneesti!')
            return redirect('/')

    else:
        form = AlbumForm()

    return render(request, 'add_album.html', {'form': form})


def search(request):
    uri = request.build_absolute_uri()
    print(uri)

    if request.method == 'GET':  # If the form is submitted
        search_term = request.GET.get('search')

        try:
            search_words = search_term.split(' ')
        except:
            messages.error(request, 'Etsiminen ei onnistunut.')
            return redirect('index')
        
        image_results = Image.objects.filter(Q(name__contains=search_words[0])
                | Q(description__contains=search_words[0]))

        if len(search_words) > 1:
            for w in search_words:
                if w != search_words[0]:
                    image_results = image_results.filter(Q(name__contains=w)
                            | Q(description__contains=w))

        context = create_pagination(request, image_results)

        context.update({"search_term": ("?search=" + search_term + "&")})

    return render(request, 'search_results.html', context)


