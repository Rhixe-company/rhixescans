# Generated by Django 4.1.3 on 2022-12-17 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0018_alter_comic_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='release_date',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
