# Generated by Django 3.1.3 on 2021-05-04 10:15

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('clusters_app', '0003_auto_20210504_1140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectionin2d',
            old_name='baseData',
            new_name='base_data',
        ),
        migrations.AddField(
            model_name='projectionin2d',
            name='data',
            field=picklefield.fields.PickledObjectField(default='SOME STRING', editable=False),
        ),
    ]