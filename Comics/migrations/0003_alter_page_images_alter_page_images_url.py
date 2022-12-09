# Generated by Django 4.1.3 on 2022-12-09 20:03

import Comics.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0002_alter_comic_options_remove_chapter_numreviews_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='images',
            field=models.ImageField(default='images/pages.jpg', max_length=10000, upload_to=Comics.models.comics_chapters_images_location),
        ),
        migrations.AlterField(
            model_name='page',
            name='images_url',
            field=models.URLField(max_length=10000),
        ),
    ]