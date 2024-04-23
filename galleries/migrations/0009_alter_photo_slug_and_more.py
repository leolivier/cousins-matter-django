# Generated by Django 5.0.2 on 2024-04-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0008_alter_gallery_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='slug',
            field=models.SlugField(blank=True, max_length=70),
        ),
        migrations.AddConstraint(
            model_name='photo',
            constraint=models.UniqueConstraint(models.F('slug'), models.F('gallery'), name='slugs must be unique inside their gallery'),
        ),
    ]
