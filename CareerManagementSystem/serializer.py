from .models import CareerCategory, Course
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'industry', 'courseName', 'bannerImage']

class CareerCategorySerializer(serializers.ModelSerializer):
    industryData = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = CareerCategory
        fields = ['id', 'industry', 'industryData']

