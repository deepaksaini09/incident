# Generated by Django 4.2.1 on 2023-06-04 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incidentapp', '0003_rename_user_id_incident_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='reported_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 4, 13, 47, 8, 668250)),
        ),
    ]