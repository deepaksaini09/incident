import datetime

from django.db import models

# Create your models here.
INCIDENT_CHOICES = (
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
)
INCIDENT_STATUS_CHOICES = (
    ('open', 'Open'),
    ('progress', 'In progres'),
    ('closed', 'Closed'),
)


class createUsersModels(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)


class incident(models.Model):
    user_id = models.IntegerField(null=False, default=1)
    incident_id = models.CharField(max_length=100, null=True)
    reporter_name = models.CharField(max_length=100)
    incident_details = models.TextField()
    reported_date = models.DateTimeField(default=datetime.datetime.now())
    priority = models.CharField(choices=INCIDENT_CHOICES, default='medium', max_length=20)
    Incident_status = models.CharField(choices=INCIDENT_STATUS_CHOICES, default='open', max_length=50)
