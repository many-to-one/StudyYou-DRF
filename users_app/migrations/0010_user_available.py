# Generated by Django 4.1.5 on 2023-03-21 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0009_remove_user_action_user_duty_user_microphones_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]
