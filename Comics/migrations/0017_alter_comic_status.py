# Generated by Django 4.1.3 on 2022-12-05 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Comics', '0016_alter_comic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completed'), ('Ongoing', 'Ongoing'), ('Dropped', 'Dropped')], default='Ongoing', max_length=100),
        ),
    ]
