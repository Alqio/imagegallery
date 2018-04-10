from django.shortcuts import render, redirect, HttpResponse
from images.models import Image, Album
from imagegallery.models import UserProfile
from hashlib import md5
import os
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def index(request):
   return HttpResponse("Moro!") 
