# Generated by Django 4.1.3 on 2022-12-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0004_alter_comic_artist_alter_comic_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='artist',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='comic',
            name='category',
            field=models.CharField(blank=True, choices=[('Manhua', 'Manhua'), ('Manhwa', 'Manhwa'), ('Manga', 'Manga')], max_length=10),
        ),
        migrations.AlterField(
            model_name='comic',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=9),
        ),
    ]