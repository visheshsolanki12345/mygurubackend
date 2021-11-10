from rest_framework import serializers
# from django.contrib.auth.models import User
from AptitueTestManagement.models import TestScheduleManagement

class TestScheduleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScheduleManagement
        fields = '__all__'
