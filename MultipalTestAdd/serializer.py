from rest_framework import serializers

from .models import (
    NewClass, ResultTitle, SelectAcademic, ShowGrade, Section, Interpretation, TestBackupFiveQuize, TestBackupMultipalQuize, TestBackupOneQuizeCorrect, TestBackupThreeQuize, Title,
     ImageOptionsTest, OneOptionsTest,
    OptionsTest, AddTest, TestCategory, ThreeOptionsTest, FiveOptionsTest, SelectNumber,
    Reports, InterpretationGrade, Career, AddClassSection, SectionInterest, CarrerDescription
    )

class SelectAcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = SelectAcademic
        fields = ['id', 'classOrCollage']

class AddClassSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddClassSection
        fields = ['id', 'classSection']

class NewClassSerializer(serializers.ModelSerializer):
    classOrCollage = SelectAcademicSerializer(many=False, read_only=True)
    class Meta:
        model = NewClass
        fields = ['id', 'newClass', 'classOrCollage']

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['id', 'newCareer']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'section', 'sectionInterest', 'number', 'duration']

class SectionInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionInterest
        fields = ['sectionInterest']

class InterpretationGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterpretationGrade
        fields = ['id', 'grade']

class TitleSerializer(serializers.ModelSerializer):
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    class Meta:
        model = Title
        fields = ['id', 'className', 'classSection', 'generalInstructions', 'description', 'duration', 'price']

class ShowGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowGrade
        fields = ['id', 'className', 'classSection', 'section', 'selectGrade', 'score', 'the_json']

class InterpretationSerializer(serializers.ModelSerializer):
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    section = SectionSerializer(many=False, read_only=True)
    grade = ShowGradeSerializer(many=False, read_only=True)
    selectGrade = InterpretationGradeSerializer(many=False, read_only=True)
    class Meta:
        model = Interpretation
        fields = ['id', 'className', 'classSection', 'section', 'grade','selectGrade', 'title', 'point', 'the_json', 'the_title']

class SelectNumberSerializer(serializers.ModelSerializer):
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    class Meta:
        model = SelectNumber
        fields = ['id','className', 'classSection', 'a', 'b', 'c', 'd', 'e', 'rightAns']

class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = ['id', 'selectTest']

class ImageOptionsTestSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False, read_only=True)
    class Meta:
        model = ImageOptionsTest
        fields = ['id', 'section', 'question', 'questionText', 'a','aText', 'b','bText', 'c', 'cText', 'd', 'dText', 'e', 'eText', 'rightAns']

class OneOptionsTestSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False, read_only=True)
    class Meta:
        model = OneOptionsTest
        fields = ['id', 'section', 'questionImage', 'question', 'a', 'b', 'c', 'd', 'rightAns']

class OptionsTestSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False, read_only=True)
    career = CareerSerializer(many=False, read_only=True)
    class Meta:
        model = OptionsTest
        fields = ['id', 'career', 'section', 'question', 'a', 'b', 'c', 'd', 'e']

class ThreeOptionsTestSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False, read_only=True)
    class Meta:
        model = ThreeOptionsTest
        fields = ['id', 'section', 'question', 'a', 'b', 'c']

class CarrerDescriptionSerializer(serializers.ModelSerializer):
    carrer = CareerSerializer(many=False, read_only=True)
    section = SectionSerializer(many=False, read_only=True)
    class Meta:
        model = CarrerDescription
        fields = ['id', 'carrer', 'section','description' ]

class FiveOptionsTestSerializer(serializers.ModelSerializer):
    section = SectionSerializer(many=False, read_only=True)
    class Meta:
        model = FiveOptionsTest
        fields = ['id', 'section', 'question', 'a', 'b', 'c', 'd', 'e']


class ResultTitleSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    class Meta:
        model = ResultTitle
        fields = ['typeOfTest', 'className', 'classSection', 'mainHeading', 'title', 'discription', 'point', 'pointDiscription', 'the_json']



class AddTestSerializer(serializers.ModelSerializer):
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    title = TitleSerializer(many=False, read_only=True)
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    selectNumber = SelectNumberSerializer(many=False, read_only=True)
    resultTitle = ResultTitleSerializer(many=False, read_only=True)
    createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = AddTest
        fields = ['id', 'className', 'classSection', 'typeOfTest', 'title', 'selectNumber', 'resultTitle', 'createAt']


class ReportsSerializer(serializers.ModelSerializer):
    interpretatio = InterpretationSerializer(many=False, read_only=True)
    carrer = CareerSerializer(many=False, read_only=True)
    class Meta:
        model = Reports
        fields = ['id','user', 'Class', 'classSection', 'carrer', 'section', 'interpretatio', 'grade', 'totalCount', 'typeOftest', 'totalNoQu']


class TestBackupOneQuizeCorrectSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    oneQuizeCorrect = OneOptionsTestSerializer(many=False, read_only=True)
    testDiscription = AddTestSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestBackupOneQuizeCorrect
        fields = ['id', 'user', 'typeOfTest', 'className', 'classSection', 'oneQuizeCorrect','testDiscription', 'userClickObj', 'lastTime', 'number']


class TestBackupOneImageQuizeCorrectSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    imageOneQuizeCorrect = ImageOptionsTestSerializer(many=False, read_only=True)
    testDiscription = AddTestSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestBackupOneQuizeCorrect
        fields = ['id', 'user', 'typeOfTest', 'className', 'classSection', 'imageOneQuizeCorrect','testDiscription', 'userClickObj', 'lastTime', 'number']


class TestBackupMultipalQuizeSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    multipalQuize = OptionsTestSerializer(many=False, read_only=True)
    testDiscription = AddTestSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestBackupMultipalQuize
        fields = ['id', 'user', 'typeOfTest', 'className', 'classSection', 'multipalQuize','testDiscription', 'userClickObj', 'lastTime', 'number']


class TestBackupFiveQuizeSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    fiveQuize = FiveOptionsTestSerializer(many=False, read_only=True)
    testDiscription = AddTestSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestBackupFiveQuize
        fields = ['id', 'user', 'typeOfTest', 'className', 'classSection', 'fiveQuize','testDiscription', 'userClickObj', 'lastTime', 'number']


class TestBackupThreeQuizeSerializer(serializers.ModelSerializer):
    typeOfTest = TestCategorySerializer(many=False, read_only=True)
    className = NewClassSerializer(many=False, read_only=True)
    classSection = AddClassSectionSerializer(many=False, read_only=True)
    threeQuize = ThreeOptionsTestSerializer(many=False, read_only=True)
    testDiscription = AddTestSerializer(many=False, read_only=True)
    # createAt = serializers.DateTimeField(format = "%B %d, %Y, %I:%M%p")
    class Meta:
        model = TestBackupThreeQuize
        fields = ['id', 'user', 'typeOfTest', 'className', 'classSection', 'threeQuize','testDiscription', 'userClickObj', 'lastTime', 'number']



