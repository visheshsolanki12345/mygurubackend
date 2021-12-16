from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import TestScheduleManagement, QuestionManagement, TestResult, IndustryCategory, Grade
from .models import DefineClasses, IndustryCategory, Reports_8th, Test, Questions, ShowGrade, Interpretation_8th, GeneralInformation_8th

class DefineClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefineClasses
        fields = ['id', 'Class','testInstruction']

class TestSerializer(serializers.ModelSerializer):
    grade = DefineClassesSerializer(many=False, read_only=True)
    class Meta:
        model = Test
        fields = ['id', 'duration', 'date','amount', 'testName','grade']


class IndustryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IndustryCategory
        fields = ['id','industry_Id', 'industry']
    
class QuestionsSerializer(serializers.ModelSerializer):
    industry = IndustryCategorySerializer(many=False, read_only=True)
    class Meta:
        model = Questions
        fields = ['id', 'question', 'a', 'b', 'c', 'd','rightAns', 'industry']

class Interpretation_8thSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interpretation_8th
        fields = ['id', 'grade', 'interpretationTitle', 'YouCanDoPoint_1', 'YouCanDoPoint_2', 'YouCanDoPoint_3', 'YouCanDoPoint_4', 'YouCanDoPoint_5']


class Reports_8thSerializer(serializers.ModelSerializer):
    CreateAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    interpretatio = Interpretation_8thSerializer(many=False, read_only=True)
    class Meta:
        model = Reports_8th
        fields = ['id', 'user', 'industry', 'question', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'totalCount', 'grade', 'CreateAt', 'industry_Grade', 'interpretatio']

class ShowGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowGrade
        fields = ['id','score' , 'grade' ]

class GeneralInformation_8thSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInformation_8th
        fields = ['id','TitleImportance' ]

