from authentication.serializer import userCustomSerializer, UserSerializerWithProfile
from .models import (
    CarrerType, Carrer, CarrerPage, StudentFeaturedArticle, 
    EditorApproveArticle, Counsellor, CounsellorSlot, BookUserSlot,
    ArticleRating, ArticleNoView
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
        fields = ['id', 'carrer', 'heading', 'bannerImage', 'thumbnailImage', 'description']


class StudentFeaturedArticleSerializer(serializers.ModelSerializer):
    carrer = CarrerSerializer(many=False, read_only=True)
    class Meta:
        model = StudentFeaturedArticle
        fields = ['id', 'user', 'carrer', 'title', 'heading', 'description', 'bannerImage', 'thumbnailImage', 'articleApprove', 'createAt']


class EditorApproveArticleSerializer(serializers.ModelSerializer):
    studentArticle = StudentFeaturedArticleSerializer(many=False, read_only=True)
    user = userCustomSerializer(many=False, read_only=True)
    class Meta:
        model = EditorApproveArticle
        fields = [
            'id', 'user', 'studentArticle', 'paymentChoices', 'articleApprove', 
            'ammount', 'createAt', 'createAt', 'rating', 'noView',
        ]

class CounsellorSerializer(serializers.ModelSerializer):
    carrer = CarrerSerializer(many=False, read_only=True)
    user = UserSerializerWithProfile(many=False, read_only=True)
    class Meta:
        model = Counsellor
        fields = [
            'id', 'user', 'carrer', 'title', 'qualification', 'mobile', 'experience', 
            'college', 'designation', 'address', 'pincode', 'area', 'aboutUs', 
            'language', 'price', 'dateOfBirth', 'gender', 'createAt', 'bannerImage',
            'rating', 'noView',
        ]


class CounsellorSlotSerializer(serializers.ModelSerializer):
    # counsellor = CounsellorSerializer(many=False, read_only=True)
    # date = serializers.DateField(format="%d/%m/%Y")
    timeFrom = serializers.TimeField(format="%H:%M")
    timeTo = serializers.TimeField(format="%H:%M")
    class Meta:
        model = CounsellorSlot
        fields = ['id', 'counsellor', 'date', 'timeFrom', 'timeTo', 'isBook']


class BookUserSlotSerializer(serializers.ModelSerializer):
    counsellorSlot = CounsellorSlotSerializer(many=False, read_only=True)
    class Meta:
        model = BookUserSlot
        fields = ['id', 'user', 'counsellorSlot']