# Generated by Django 2.1.7 on 2019-03-21 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classified_ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
