# Generated by Django 2.1.7 on 2019-05-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_rstatus_statetext'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission_queue',
            name='robot_queue_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
