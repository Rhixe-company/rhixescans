# Generated by Django 4.1.3 on 2022-12-15 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0003_comic_image_url_alter_comic_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='image_url',
            new_name='image_src',
        ),
    ]
