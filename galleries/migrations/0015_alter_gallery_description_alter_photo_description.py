# Generated by Django 5.0.6 on 2024-05-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0014_alter_photo_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='description',
            field=models.TextField(blank=True, max_length=3000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(blank=True, max_length=3000, verbose_name='Description'),
        ),
    ]
