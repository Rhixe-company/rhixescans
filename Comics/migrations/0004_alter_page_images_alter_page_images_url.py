# Generated by Django 4.1.3 on 2022-12-09 18:01

import Comics.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0003_alter_chapter_options_remove_genre_comics_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='images',
            field=models.ImageField(max_length=10000, upload_to=Comics.models.comics_chapters_images_location),
        ),
        migrations.AlterField(
            model_name='page',
            name='images_url',
            field=models.URLField(blank=True, max_length=10000, null=True),
        ),
    ]
