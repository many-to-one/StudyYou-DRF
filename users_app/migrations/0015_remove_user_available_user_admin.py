# Generated by Django 4.1.5 on 2023-03-24 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0014_user_ministry_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='available',
        ),
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
    ]
