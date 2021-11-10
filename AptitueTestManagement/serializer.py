from rest_framework import serializers
# from django.contrib.auth.models import User
from AptitueTestManagement.models import TestScheduleManagement, QuestionManagement

class TestScheduleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScheduleManagement
        fields = '__all__'

class QuestionManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionManagement
        fields = '__all__'
