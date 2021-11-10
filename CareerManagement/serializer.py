from rest_framework import serializers
from django.contrib.auth.models import User
from CareerManagement.models import Industry

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = '__all__'
    
# class StudentQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudentQuestion
#         fields = '__all__'
