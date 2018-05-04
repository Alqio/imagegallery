from django.conf.urls import url
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('albums/', views.albums, name='albums'),
    path('add_album/', views.add_album, name='add_album'),
    path('add_image/', views.add_image, name='add_image'),
    path('album/<int:id>/', views.view_album, name='view_album'),
    path('image/<slug:name>/', views.view_image, name='view_image'),
    path('album/<int:album_id>/image/<int:id>/', views.view_image, name='view_image')
]


if settings.DEBUG: 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

