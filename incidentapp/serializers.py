from rest_framework import serializers
from .models import createUsersModels, incident


class usersSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return createUsersModels.objects.create(**validated_data)


class incidentSerializers(serializers.Serializer):
    user_id = serializers.IntegerField()
    incident_id = serializers.CharField(max_length=100)
    reporter_name = serializers.CharField(max_length=100)
    incident_details = serializers.CharField()
    reported_date = serializers.DateTimeField()
    priority = serializers.CharField(max_length=20)
    Incident_status = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return incident.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # print(validated_data, instance.incident_details)
        print(instance.Incident_status)
        instance.incident_details = validated_data.get('incident_details', instance.incident_details)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.Incident_status = validated_data.get('Incident_status', instance.Incident_status)
        instance.save()
        return instance





