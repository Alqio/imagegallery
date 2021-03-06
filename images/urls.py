from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('albums/', views.albums, name='albums'),
    path('search_results/', views.search, name="search"),
    path('add_album/', views.add_album, name='add_album'),
    path('add_image/', views.add_image, name='add_image'),
    path('album/<int:id>/', views.view_album, name='view_album'),
    path('image/<int:id>/', views.view_image, name='view_image'),
    path('album/<int:album_id>/image/<int:id>/', views.view_image, name='view_image'),
    path('image/edit/<int:image_id>/', views.edit_image, name='edit_image'),
    path('image/remove/<int:image_id>/', views.remove_image, name='remove_image'),
    path('album/remove/<int:album_id>/', views.remove_album, name='remove_album'),
    path('album/edit/<int:album_id>/', views.edit_album, name='edit_album'),
    path('about/', views.about, name='about'),
    path('sign_s3/', views.sign_s3, name='sign_s3')
]
