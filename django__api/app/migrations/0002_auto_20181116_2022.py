# Generated by Django 2.1.3 on 2018-11-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.TextField(blank=True, max_length=100),
        ),
    ]