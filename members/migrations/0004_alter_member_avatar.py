# Generated by Django 5.0.2 on 2024-04-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_address_options_alter_family_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='avatar',
            field=models.ImageField(blank=True, default='/static/members/images/default-avatar.jpg', upload_to='avatars'),
        ),
    ]