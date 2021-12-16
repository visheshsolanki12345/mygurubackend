from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import TestScheduleManagement, QuestionManagement, TestResult, IndustryCategory, ShowGrade


class TestScheduleManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestScheduleManagement
        fields = ['id', 'duration', 'date','amount', 'testName','grade']

class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory
        fields = ['id', 'industry_Id', 'industry']

class QuestionManagementSerializer(serializers.ModelSerializer):
    industry = IndustryCategorySerializer(many=False, read_only=True)
    class Meta:
        model = QuestionManagement
        fields = ['id', 'question', 'a', 'b', 'c', 'd', 'e', 'industry']


class TestResultSerializer(serializers.ModelSerializer):
    CreateAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestResult
        fields = ['id', 'user', 'industry', 'question', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'totalCount', 'grade', 'CreateAt', 'industry_Grade']

class ShowGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowGrade
        fields = ['id','score' , 'grade' ]