from django.db import models
from PIL import Image as PilImage


class Image(models.Model):
    name = models.CharField(max_length=30, unique=True)
    uploaded = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=255)
    # the user id of the uploader
    uploader = models.IntegerField()
    pic = models.ImageField(upload_to='images/', default='images/default_image.png')
    views = models.IntegerField()

    compressed_pic = models.ImageField(upload_to='images/', default='images/default_image.png')

    def __str__(self):
        return self.name

    def create_compressed_pic(self):
        print("size:", self.pic.size)
        pil_pic = PilImage.open(self.pic)

        print(pil_pic)
        (width, height) = pil_pic.size
        print(width, height)

        cropped = pil_pic.resize((int(width/4), int(height/4)), PilImage.ANTIALIAS)
        cropped.save(self.compressed_pic)


class Album(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=255)
    creator = models.IntegerField()
    images = models.ManyToManyField(Image) 

    def __str__(self):
        return self.name
