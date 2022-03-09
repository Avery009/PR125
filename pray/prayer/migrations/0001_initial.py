# Generated by Django 4.0.3 on 2022-03-09 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prayer',
            fields=[
                ('prayer_id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('prayer_title', models.CharField(max_length=100)),
                ('prayer_request_date', models.DateTimeField()),
                ('prayer_description', models.CharField(max_length=1000)),
                ('prayer_count', models.IntegerField()),
            ],
        ),
    ]