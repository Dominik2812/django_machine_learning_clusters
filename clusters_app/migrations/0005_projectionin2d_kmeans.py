# Generated by Django 3.1.3 on 2021-05-04 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clusters_app', '0004_auto_20210504_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectionin2d',
            name='kmeans',
            field=models.BooleanField(default=False),
        ),
    ]