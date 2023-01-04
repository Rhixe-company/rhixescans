# Generated by Django 4.1.5 on 2023-01-04 06:00

import Comics.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0007_remove_chapter_participants_remove_comic_reader_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='images',
            field=models.ImageField(default=None, max_length=10000, null=True, unique=True, upload_to=Comics.models.comics_chapters_images_location),
        ),
        migrations.AlterField(
            model_name='page',
            name='images_url',
            field=models.URLField(blank=True, default=None, max_length=10000, null=True, unique=True),
        ),
    ]
