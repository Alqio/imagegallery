# Generated by Django 2.0.4 on 2018-05-27 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='pic',
            field=models.URLField(max_length=400),
        ),
    ]