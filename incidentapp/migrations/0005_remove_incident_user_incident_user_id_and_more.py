# Generated by Django 4.2.1 on 2023-06-04 14:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidentapp', '0004_alter_incident_reported_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incident',
            name='user',
        ),
        migrations.AddField(
            model_name='incident',
            name='user_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='incident',
            name='reported_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 4, 14, 44, 33, 386555)),
        ),
    ]