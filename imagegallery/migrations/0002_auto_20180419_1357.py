# Generated by Django 2.0.4 on 2018-04-19 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagegallery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminuserprofile',
            name='uploaded_images',
        ),
        migrations.RemoveField(
            model_name='adminuserprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='AdminUserProfile',
        ),
    ]