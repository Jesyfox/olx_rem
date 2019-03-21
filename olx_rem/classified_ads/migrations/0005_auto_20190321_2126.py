# Generated by Django 2.1.7 on 2019-03-21 21:26

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classified_ads', '0004_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photos',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/photos'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
