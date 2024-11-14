# Generated by Django 5.1.3 on 2024-11-12 19:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_wrap'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='wraps',
            field=models.ManyToManyField(blank=True, to='users.wrap'),
        ),
        migrations.AddField(
            model_name='wrap',
            name='top_artists',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='wrap',
            name='top_tracks',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='wrap',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]