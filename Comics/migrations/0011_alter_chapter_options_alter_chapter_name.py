# Generated by Django 4.1.3 on 2022-12-02 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0010_remove_chapter_volume'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['created']},
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=1000, null=True, unique=True),
        ),
    ]
