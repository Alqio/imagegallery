from django.db import models
from PIL import Image as PilImage
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.utils.crypto import get_random_string


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

    def save(self):

        file_name = self.pic.name

        unique_id = get_random_string(length=8)

        file_parts = file_name.split('.', len(file_name))
        file_name = file_parts[0] + unique_id + "." + file_parts[1]

        self.pic.name = file_name

        im = PilImage.open(self.pic)

        w, h = im.size

        output = BytesIO()

        compressed_im = im.resize((int(w/4), int(h/4)), PilImage.ANTIALIAS)
        compressed_im.save(output, format='PNG', quality=70)
        output.seek(0)

        self.compressed_pic = InMemoryUploadedFile(output, 'ImageField', self.pic.name.split('.')[0] + "_compressed.png",
                                                   'image/png', sys.getsizeof(output), None)

        super(Image, self).save()


class Album(models.Model):
    name = models.CharField(max_length=30, unique=True)
    created = models.DateField(auto_now=False, auto_now_add=True)
    description = models.CharField(max_length=255)
    creator = models.IntegerField()
    images = models.ManyToManyField(Image) 

    def __str__(self):
        return self.name
