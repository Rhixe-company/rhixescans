# Generated by Django 4.1.3 on 2022-12-15 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0009_comicsmanager'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comicsmanager',
            options={'ordering': ['title']},
        ),
    ]
