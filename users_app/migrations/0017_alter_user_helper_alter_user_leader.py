# Generated by Django 4.1.5 on 2023-03-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0016_alter_user_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='helper',
            field=models.BooleanField(default=False, verbose_name='Helper (lector, service)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='leader',
            field=models.BooleanField(default=False, verbose_name='Leader'),
        ),
    ]