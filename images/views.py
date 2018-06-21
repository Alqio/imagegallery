from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from images.models import Image, Album
from imagegallery.models import UserProfile
from images.forms import ImageForm, AlbumForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.utils.crypto import get_random_string
from botocore.client import Config

import os
import boto3


def about(request):
    return render(request, 'about.html')


def create_pagination(request, items_all, item_name='items'):
    nof_items_per_page = 24

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

    # count works only on django query sets
    # len has to be used if items_all is a regular list 
    try:
        amount = items_all.count()
    except:
        amount = len(items_all)

    context = {
        item_name: items,
        'pages': p.page_range,
        'current_page': page,
        'amount': amount,
        'search_term': '?'
    }

    return context


def index(request):
    images = Image.objects.all().order_by("-id")[:24]
    context = create_pagination(request, images)
    items_amount = len(context["items"])

    print("items amount", items_amount)

    context["items"] = zip(context["items"], list(range(0, items_amount)))

    return render(request, 'index.html', context)


def albums(request):

    albums_all = Album.objects.all()
    
    items_all = []
 
    for album in albums_all:
        try:
            image = album.images.latest('uploaded').compressed_pic.url
            print(image)
        except:
            image = "https://" + os.environ.get("S3_BUCKET") + ".s3.amazonaws.com/media/images/default_image.png"

        pair = (album, image)
        items_all.append(pair)

    context = create_pagination(request, items_all)
    return render(request, 'albums.html', context)


def view_album(request, id):

    try:
        album = Album.objects.get(pk=id)
    except:
        return redirect('/')

    images_all = album.images.all()
    context = create_pagination(request, images_all)
    items_amount = len(context["items"])
    context["items"] = zip(context["items"], list(range(0, items_amount)))
    context.update({'album': album})

    return render(request, 'album_photoswipe.html', context)


def view_image(request, id):
    
    try:
        image = Image.objects.get(pk=id)
    except:
        return redirect('/')
   
    try:
        uploader = UserProfile.objects.get(pk=image.uploader).user.username
    except:
        uploader = "Tuntematon"

    albums = Album.objects.all()
    belongs_to = []

    for a in albums:
        if image in a.images.all():
            belongs_to.append(a)

    context = {
        'image': image,
        'uploader': uploader,
        'albums': belongs_to
    }

    return render(request, 'image.html', context)


def sign_s3(request):
    S3_BUCKET = os.environ.get('S3_BUCKET')
    print(S3_BUCKET)

    file_name = request.GET.get('file_name')
    file_type = request.GET.get('file_type')

    # this makes sure that things won't get replaced in S3
    unique_id = get_random_string(length=8)
    
    file_parts = file_name.split('.', len(file_name))
    file_name = file_parts[0] + unique_id + "." + file_parts[1]
    
    print('in sign_s3, file: ', file_name, file_type)

    s3 = boto3.client('s3', 'eu-west-3', config=Config(signature_version='s3v4'))

    presigned_post = s3.generate_presigned_post(
        Key = file_name,
        Bucket = S3_BUCKET,
        Fields = {"Content-Type": file_type},
        Conditions = [
          {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    url = 'https://s3.eu-west-3.amazonaws.com/' + S3_BUCKET + '/' + file_name 

    ret = JsonResponse({'data': presigned_post, 'url': url})
    return ret


def add_image(request):

    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu siään lisätäksesi kuvia')
        return redirect('/')

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user.id

            try:
                pic = request.FILES['pic']
                image.pic = pic

                # image_file = io.StringIO(pic.read())
                # pil_image = PilImage.open(image_file)
                # w, h = pil_image.size
                #
                # pil_image = pil_image.resize((w/4, h/4), PilImage.ANTIALIAS)
                # image_file = io.StringIO()
                # pil_image.save(image_file, 'PNG', quality=90)
                #
                # image.compressed_pic = image_file

            except Exception as e:
                print(e)
                messages.info(request, 'Kuvalle ei annettu kuvaa, käytetään oletusta.')
                print("No pic provided, using default image.")

            image.views = 0
            image.save()

            album = Album.objects.get(pk=request.POST['album'])
            album.images.add(image)
            album.save()
            form = ImageForm()

            messages.success(request, 'Kuva ladattiin onnistuneesti!')
        
    else:
        form = ImageForm()

    return render(request, 'add_image.html', {'form': form})


def remove_image(request, image_id):

    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu siään poistaaksesi kuvia')
        return redirect('/')

    image = Image.objects.get(id=image_id)

    if image is None:
        messages.error(request, 'Kuvan poistaminen epäonnistui')
        return redirect('/')

    for album in Album.objects.all():
        if image in album.images.all():
            album.images.remove(image)
            break

    image.delete()

    messages.success(request, 'Kuva poistettiin onnistuneesti')
    return redirect('/')


def edit_image(request, image_id):

    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu siään muokataksesi kuvia')
        return redirect('/')

    image = Image.objects.get(id=image_id)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():

            image.name = form.cleaned_data['name']
            image.description = form.cleaned_data['description']

            if request.FILES['pic']:
                image.pic = request.FILES['pic']

            messages.success(request, 'Kuvaa muokattiin onnistuneesti')

    else:
        form = ImageForm(None, instance=image)

    return render(request, 'edit_image.html', {'form': form})


def add_album(request):

    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu siään lisätäksesi albumeja')
        return redirect('/')

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


def remove_album(request, album_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu sisään poistaaksesi albumeja')
        return redirect('/')

    album = Album.objects.get(id=album_id)

    for image in album.images.all():
        image.delete()

    album.delete()

    messages.success(request, 'Albumi poistettiin onnistuneesti')
    return redirect('/')


def edit_album(request, album_id):

    if not request.user.is_authenticated:
        messages.error(request, 'Kirjaudu siään muokataksesi albumeja')
        return redirect('/')

    album = Album.objects.get(pk=album_id)

    if request.method == 'POST':
        form = AlbumForm(request.POST)

        if form.is_valid():

            album.name = form.cleaned_data['name']
            album.description = form.cleaned_data['description']

            messages.success(request, 'Albumia muokattiin onnistuneesti')

    else:
        form = ImageForm(None, instance=album)

    context = {
        'form': form,
        'album': album,
        'count': album.images.count()
    }

    return render(request, 'edit_album.html', context)


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

