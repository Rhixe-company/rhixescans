# Generated by Django 4.1.5 on 2023-01-11 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='numChapters',
        ),
        migrations.AlterField(
            model_name='page',
            name='images_url',
            field=models.URLField(blank=True, max_length=10000),
        ),
    ]