# Generated by Django 4.1.3 on 2022-12-02 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0013_alter_chapter_options_alter_comic_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comic',
            options={'ordering': ['-updated']},
        ),
    ]
