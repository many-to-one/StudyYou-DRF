# Generated by Django 4.1.5 on 2023-03-26 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0015_remove_user_available_user_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='service',
            field=models.BooleanField(default=False, verbose_name='Service (microphones, music, duty)'),
        ),
    ]
