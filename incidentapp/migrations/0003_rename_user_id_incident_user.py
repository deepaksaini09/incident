# Generated by Django 4.2.1 on 2023-06-04 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incidentapp', '0002_incident'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incident',
            old_name='user_id',
            new_name='user',
        ),
    ]
