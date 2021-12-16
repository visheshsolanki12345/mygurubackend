from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import DefineClasses, IndustryCategory, Interpretation_10th_int, Reports_10th_int, Test, Questions, ShowGrade, GeneralInformation_10th_Int

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
        fields = ['id', 'question', 'a', 'b', 'c', 'd', 'e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t', 'industry']

class Interpretation_10th_intSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interpretation_10th_int
        fields = ['id', 'grade', 'interpretationTitle', 'YouCanDoPoint_1', 'YouCanDoPoint_2', 'YouCanDoPoint_3', 'YouCanDoPoint_4', 'YouCanDoPoint_5']

class Reports_10th_intSerializer(serializers.ModelSerializer):
    CreateAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    interpretatio = Interpretation_10th_intSerializer(many=False, read_only=True)
    class Meta:
        model = Reports_10th_int
        fields = ['id', 'user', 'industry', 'question', 'ans1', 'ans2', 'ans3', 'ans4', 'ans5', 'totalCount', 'grade', 'CreateAt', 'industry_Grade', 'interpretatio']

class ShowGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowGrade
        fields = ['id','area', 'score', 'HigeScore',  'grade' ]


class GeneralInformation_10th_IntSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralInformation_10th_Int
        fields = ['id','TitleImportance' ]