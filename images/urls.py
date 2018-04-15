from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add_album', views.add_album, name='add_album'),
    url(r'^add_image', views.add_image, name='add_image')
]

