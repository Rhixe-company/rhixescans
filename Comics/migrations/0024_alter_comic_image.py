# Generated by Django 4.1.3 on 2022-12-18 17:06

import Comics.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0023_comic_reader_remove_comic_user_comic_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='image',
            field=models.ImageField(upload_to=Comics.models.comics_images_location),
        ),
    ]