# Generated by Django 3.1.3 on 2021-05-04 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clusters_app', '0002_projectionin2d'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectionin2d',
            name='dimRed',
        ),
        migrations.RemoveField(
            model_name='projectionin2d',
            name='model',
        ),
    ]