# Generated by Django 5.1.1 on 2024-10-29 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='Anonymous', max_length=100),
        ),
    ]
