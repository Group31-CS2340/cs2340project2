# Generated by Django 5.1.2 on 2024-11-28 21:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_slidedata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SlideData',
        ),
    ]