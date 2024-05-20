# Generated by Django 5.0.6 on 2024-05-19 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0006_alter_member_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('content', models.TextField(max_length=1048576, verbose_name='Content')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('reply_to', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.newscontent')),
            ],
            options={
                'ordering': ['reply_to', 'date'],
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Title')),
                ('first_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.newscontent')),
            ],
            options={
                'verbose_name_plural': 'news',
                'ordering': ['first_content__date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('content', models.CharField(max_length=1000, verbose_name='Comment')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
                ('news_content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.newscontent')),
            ],
            options={
                'verbose_name_plural': 'comments',
                'ordering': ['news_content', 'date'],
            },
        ),
        migrations.AddIndex(
            model_name='newscontent',
            index=models.Index(fields=['reply_to', 'author'], name='news_newsco_reply_t_ed2499_idx'),
        ),
        migrations.AddIndex(
            model_name='news',
            index=models.Index(fields=['title'], name='news_news_title_ef31ad_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['news_content', 'author'], name='news_commen_news_co_318794_idx'),
        ),
    ]