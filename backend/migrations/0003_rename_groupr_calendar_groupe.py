# Generated by Django 4.1.5 on 2023-03-16 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_calendar_groupr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendar',
            old_name='groupr',
            new_name='groupe',
        ),
    ]
