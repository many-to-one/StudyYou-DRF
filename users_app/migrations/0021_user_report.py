# Generated by Django 4.1.5 on 2023-04-02 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0020_user_editor'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='report',
            field=models.BooleanField(default=False, verbose_name='Report'),
        ),
    ]
