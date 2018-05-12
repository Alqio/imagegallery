from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.api_index, name='api_index'),
    url(r'^checkusername/$', views.check_username, name='check_username'),
    url(r'^checkloginusername/$', views.check_login_username, name='check_login_username'),
    path('album/<int:album_id>/', views.get_album_images,
        name="get_album_images"),
    path('index/', views.get_index_images, name="get_index_images")
]

