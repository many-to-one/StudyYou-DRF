# Generated by Django 4.1.5 on 2023-03-17 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_calendar_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='months',
            name='studies',
            field=models.IntegerField(default=0),
        ),
    ]
