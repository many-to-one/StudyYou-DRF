# Generated by Django 4.1.5 on 2023-03-27 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_calendar_arr_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendar',
            name='check_arr_icon',
            field=models.BooleanField(default=False),
        ),
    ]