from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from imagegallery.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

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

