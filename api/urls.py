from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.api_index, name='api_index'),
    url(r'^checkusername/$', views.check_username, name='check_username'),
    url(r'^checkloginusername/$', views.check_login_username, name='check_login_username'),
]

