from django.db import models

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=30, unique=True)
    uploaded = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=255)
    # the user id of the uploader
    uploader = models.IntegerField()
    pic = models.ImageField(upload_to='images/',
            default='images/default_image.png')


class Album(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=255)
    creator = models.IntegerField()
    images = models.ManyToManyField(Image) 

    def __str__(self):
        return self.name
