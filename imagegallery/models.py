from django.db import models
from django.contrib.auth.models import User
from images.models import Image

class UserProfile(models.Model):
    """
    Model for the users of the store.

    user = Django's own User object, used for logging in to the store and fields such as username.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uploaded_images = models.ManyToManyField(Image)
    is_admin = models.BooleanField()	
