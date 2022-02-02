from .models import (
    CarrerType, Carrer, CarrerPage, StudentFeaturedArticle, 
    EditorApproveArticle, Counsellor, CounsellorSlot, BookUserSlot
)

from rest_framework import serializers

class CarrerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarrerType
        fields = ['id', 'typeOfCarrer']


class CarrerSerializer(serializers.ModelSerializer):
    carrerType = CarrerTypeSerializer(many=False, read_only=True)
    class Meta:
        model = Carrer
        fields = ['id', 'carrerType', 'carrer']


class CarrerPageSerializer(serializers.ModelSerializer):
    carrer = CarrerSerializer(many=False, read_only=True)
    class Meta:
        model = CarrerPage
        fields = ['id', 'carrer', 'heading', 'bannerImage', 'description']


class StudentFeaturedArticleSerializer(serializers.ModelSerializer):
    carrer = CarrerSerializer(many=False, read_only=True)
    class Meta:
        model = StudentFeaturedArticle
        fields = ['id', 'user', 'carrer', 'heading', 'description', 'bannerImage', 'articleApprove', 'createAt']


class EditorApproveArticleSerializer(serializers.ModelSerializer):
    studentArticle = StudentFeaturedArticleSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = EditorApproveArticle
        fields = [
            'id', 'user', 'studentArticle', 'paymentChoices', 'articleApprove', 
            'ammount', 'createAt', 'createAt'
        ]

class CounsellorSerializer(serializers.ModelSerializer):
    carrer = CarrerSerializer(many=False, read_only=True)
    class Meta:
        model = Counsellor
        fields = [
            'id', 'user', 'carrer', 'title', 'qualification', 'mobile', 'experience', 
            'college', 'designation', 'address', 'pincode', 'area', 'aboutUs', 
            'language', 'price', 'dateOfBirth', 'gender', 'createAt'
        ]


class CounsellorSlotSerializer(serializers.ModelSerializer):
    carrer = CounsellorSerializer(many=False, read_only=True)
    class Meta:
        model = CounsellorSlot
        fields = ['id', 'counsellor', 'date', 'timeFrom', 'timeTo', 'isBook']


class BookUserSlotSerializer(serializers.ModelSerializer):
    carrer = CounsellorSerializer(many=False, read_only=True)
    class Meta:
        model = BookUserSlot
        fields = ['id', 'user', 'counsellorSlot']