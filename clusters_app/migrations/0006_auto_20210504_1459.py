# Generated by Django 3.1.3 on 2021-05-04 12:59

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clusters_app', '0005_projectionin2d_kmeans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectionin2d',
            name='kmeans',
            field=picklefield.fields.PickledObjectField(default='SOME STRING', editable=False),
        ),
    ]