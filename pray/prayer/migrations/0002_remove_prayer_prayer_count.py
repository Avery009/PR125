# Generated by Django 4.0.3 on 2022-03-09 03:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prayer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prayer',
            name='prayer_count',
        ),
    ]
