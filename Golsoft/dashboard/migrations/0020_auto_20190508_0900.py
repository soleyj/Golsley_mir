# Generated by Django 2.1.7 on 2019-05-08 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_rstatus_mission_queue_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rstatus',
            name='mission_queue_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
