# Generated by Django 4.1.5 on 2023-04-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0022_user_stand'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lector',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='helper',
            field=models.BooleanField(default=False, verbose_name='Helper (service, prayers)'),
        ),
    ]