# Generated by Django 5.0.6 on 2024-05-19 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_alter_member_birthdate'),
        ('news', '0003_alter_newscontent_reply_to'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='newscontent',
            name='news_newsco_reply_t_ed2499_idx',
        ),
        migrations.RenameField(
            model_name='newscontent',
            old_name='reply_to',
            new_name='news',
        ),
        migrations.AlterField(
            model_name='news',
            name='first_content',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_first', to='news.newscontent'),
        ),
        migrations.AddIndex(
            model_name='newscontent',
            index=models.Index(fields=['news', 'author'], name='news_newsco_news_id_68bba4_idx'),
        ),
    ]
