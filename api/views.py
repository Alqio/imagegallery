from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from images.models import Album, Image


def api_index(request):
    return HttpResponse("This is the root of API.")


def check_username(request):
    """
    Checks the current user's username's availability.
    """
    if request.GET.get('user'):
        user = request.GET['user']
        print(user)
        if User.objects.filter(username=user).count():
            return JsonResponse({'success': False})
        return JsonResponse({'success': True})


def check_login_username(request):
    """
    Checks if login username is correct.
    """
    if request.GET.get('user'):
        user = request.GET['user']
        print(user)
        if User.objects.filter(username=user).count():
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


def get_album_images(request, album_id):
    if request.method == 'GET':
        album = Album.objects.get(id=album_id)
        images = album.images.all()
        image_list = []

        for image in images:
            try:
                dd = {
                    'image': {
                        'name': image.name,
                        'description': image.description,
                        'width': image.pic.width,
                        'height': image.pic.height,
                        'pic': image.pic.url
                    }
                }
                image_list.append(dd)
            except:
                print("Failed to display image", image)

        result = JsonResponse({'results': image_list})
        
        print(result)

        return result 


def get_index_images(request):
    if request.method == "GET":
        images = Image.objects.all().order_by('-id')[:12]
        
        image_list = []
 
        for image in images:
            try:
                dd = {
                    'image': {
                        'name': image.name,
                        'description': image.description,
                        'width': image.pic.width,
                        'height': image.pic.height,
                        'pic': image.pic.url
                    }
                }
                image_list.append(dd)
            except:
                print("Failed to display image", image)

        result = JsonResponse({'results': image_list})
        
        return result 

