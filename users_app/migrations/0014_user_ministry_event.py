# Generated by Django 4.1.5 on 2023-03-23 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0013_user_leader'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='ministry_event',
            field=models.BooleanField(default=False),
        ),
    ]
