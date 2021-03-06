from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
import jsonfield
from django_mysql.models import ListCharField
from django.db.models import CharField, Model
from django_mysql.models import ListF
from django.contrib.auth.models import User
from tinymce.models import HTMLField
# Create your models here.


class SelectAcademic(models.Model):
    classOrCollage = models.CharField(max_length=400,null=True, blank=True)
    class Meta: 
        verbose_name_plural = "Add Working Professional & College"
    def __str__(self):
        return str(self.classOrCollage)


class AddClassSection(models.Model):
    classSection = models.CharField(max_length=400,null=True, blank=True)
    def __str__(self):
        return str(self.classSection)

class NewClass(models.Model):
    classOrCollage = models.ForeignKey(SelectAcademic,on_delete=CASCADE,max_length=400, null=True, blank=True)
    newClass = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Classes"
    def __str__(self):
        return str(f"{self.newClass} th")


class Career(models.Model):
    newCareer = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Career"
    def __str__(self):
        return str(self.newCareer)
    
class Title(models.Model):
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    generalInstructions = HTMLField(null=True, blank=True)
    duration = models.CharField(max_length=200,null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Test Title of Classes"
    def __str__(self):
        return str(f"{self.className} - {self.classSection}")

class SectionInterest(models.Model):
    sectionInterest = models.CharField(max_length=400, null=True, blank=True)

class Section(models.Model):
    section = models.CharField(max_length=400, null=True, blank=True) 
    sectionInterest = models.BooleanField(default=False)
    duration = models.CharField(max_length=200,null=True, blank=True)
    number = models.FloatField(null=True, blank=True)
    def save(self, *args, **kwargs):
        if self.sectionInterest == True:
            SectionInterest.objects.create(sectionInterest = self.section)
        super(Section, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Add Section"
    def __str__(self):
        return str(self.section)

class InterpretationGrade(models.Model):
    grade = models.CharField(max_length=400,null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Grades Name"
    def __str__(self):
        return str(self.grade)

class ShowGrade(models.Model):
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=CASCADE, null=True, blank=True)
    selectGrade = models.ForeignKey(InterpretationGrade,on_delete=CASCADE,max_length=400, null=True, blank=True)
    score = models.CharField(max_length=400, null=True, blank=True)
    the_json = jsonfield.JSONField()
    class Meta:
        verbose_name_plural = "Add Grades Marking"
    def save(self, *args, **kwargs):
        the_json = {}
        op = ShowGrade.objects.filter(className = self.className, section = self.section, classSection = self.classSection)
        if op:
            for i in op:
                json = i.the_json
                the_json = json
                the_json[str(self.selectGrade)] = self.score
            ShowGrade.objects.filter(id = i.id).update(the_json = the_json, score = '')
            return ShowGrade
        else:
            the_json[str(self.selectGrade)] = self.score
            self.the_json = the_json
            self.score = ''
            super(ShowGrade, self).save(*args, **kwargs)
    def __str__(self):
        return str(f"{self.className} - {self.classSection} - {self.section}")
    

class Interpretation(models.Model):
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)    
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    grade = models.ForeignKey(ShowGrade,on_delete=CASCADE,max_length=400, null=True, blank=True)
    selectGrade = models.ForeignKey(InterpretationGrade,on_delete=CASCADE,max_length=400, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    point = models.CharField(max_length=400, null=True, blank=True)
    the_json = jsonfield.JSONField()
    the_title = jsonfield.JSONField()
    class Meta:
        verbose_name_plural = "Add Grades Wise Interpretation"
    def save(self, *args, **kwargs):
        the_json = {}
        the_title = {}
        op = Interpretation.objects.filter(className = self.className, section = self.section, grade=self.grade, classSection = self.classSection)
        if op:
            for i in op:
                the_json = i.the_json
                the_title = i.the_title
            try:
                va = the_json[str(self.selectGrade)]
                the_json[str(self.selectGrade)] = f"{va} <==> {self.point}"
            except:
                the_json[str(self.selectGrade)] = self.point
                the_title[str(self.selectGrade)] = self.title
                self.point = ''
                self.title = ''
            Interpretation.objects.filter(id = i.id).update(the_json = the_json, the_title = the_title)
            return 
        else:
            the_json[str(self.selectGrade)] = self.point
            the_title[str(self.selectGrade)] = self.title
            self.the_json = the_json
            self.the_title = the_title
            self.point = ''
            self.title = ''
            super(Interpretation, self).save(*args, **kwargs)
    def __str__(self):
        return str(f"{self.className} - {self.classSection}")


    # point = ListCharField(base_field=CharField(max_length=10),size=6,max_length=(6 * 11),)
    # def save(self, *args, **kwargs):
    #     op = Interpretation.objects.filter(className = self.className) & Interpretation.objects.filter(section = self.section)
    #     if op:
    #         op.update(point = ListF('point').append(self.point))
    #         return Interpretation
    #     else:
    #         super(Interpretation, self).save(*args, **kwargs)
    # def __str__(self):
    #     return str(self.id)


class SelectNumber(models.Model):
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)        
    a = models.FloatField(null=True, blank=True)
    b = models.FloatField(null=True, blank=True)
    c = models.FloatField(null=True, blank=True)
    d = models.FloatField(null=True, blank=True)
    e = models.FloatField(null=True, blank=True)
    rightAns = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Options Marking in each Questions"
    def __str__(self):
        return str(f"{self.className} - {self.classSection}")

RIGHT_ANS_CHOICES =(
    ("A", "A"),
    ("AText", "AText"),
    ("B", "B"),
    ("BText", "BText"),
    ("C", "C"),
    ("CText", "CText"),
    ("D", "D"),
    ("DText", "DText"),
    ("E", "E"),
    ("EText", "EText"),
)

class ImageOptionsTest(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    questionText = HTMLField(null=True, blank=True)
    question= models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    a = models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    aText = models.TextField(null=True, blank=True)
    b = models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    bText = models.TextField(null=True, blank=True)
    c = models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    cText = models.TextField(null=True, blank=True)
    d = models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    dText = models.TextField(null=True, blank=True)
    e = models.ImageField(upload_to = 'Image-Test', null=True, blank=True, max_length=200)
    eText = models.TextField(null=True, blank=True)
    choiceRightAns = models.CharField(choices = RIGHT_ANS_CHOICES,null=True, blank=True, max_length=300)
    rightAns = models.CharField(null=True, blank=True, max_length=300)
    class Meta:
        verbose_name_plural = "Image Test"
    
    def __str__(self):
        return str(self.section)
    

class OneOptionsTest(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    question= HTMLField( null=True, blank=True)
    questionImage = models.ImageField(upload_to = 'MultiImage', null=True, blank=True, max_length=400)
    a = models.CharField(max_length=400, null=True, blank=True)
    b = models.CharField(max_length=400, null=True, blank=True)
    c = models.CharField(max_length=400, null=True, blank=True)
    d = models.CharField(max_length=400, null=True, blank=True)
    choiceRightAns = models.CharField(choices = RIGHT_ANS_CHOICES,null=True, blank=True, max_length=300)
    rightAns = models.CharField(null=True, blank=True, max_length=300)
    class Meta:
        verbose_name_plural = "Add Single Marking Type Test"
    def save(self, *args, **kwargs):
        if self.choiceRightAns == 'A':
            self.rightAns = self.a
        elif self.choiceRightAns == 'B':
            self.rightAns = self.b
        elif self.choiceRightAns == 'C':
            self.rightAns = self.c
        elif self.choiceRightAns == 'D':
            self.rightAns = self.d
        elif self.choiceRightAns == 'E':
            self.rightAns = self.e
        super(OneOptionsTest, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.section)
    

class OptionsTest(models.Model):
    career = models.ForeignKey(Career,on_delete=CASCADE,max_length=400, null=True, blank=True)
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    question= HTMLField(max_length=400, null=True, blank=True)
    a = models.CharField(max_length=400, null=True, blank=True)
    b = models.CharField(max_length=400, null=True, blank=True)
    c = models.CharField(max_length=400, null=True, blank=True)
    d = models.CharField(max_length=400, null=True, blank=True)
    e = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Multiple Marking Type Test"
    def __str__(self):
        return str(self.section)

class FiveOptionsTest(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    question= HTMLField(max_length=400, null=True, blank=True)
    a = models.CharField(max_length=400, null=True, blank=True)
    b = models.CharField(max_length=400, null=True, blank=True)
    c = models.CharField(max_length=400, null=True, blank=True)
    d = models.CharField(max_length=400, null=True, blank=True)
    e = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Five Options Type Test"
    def __str__(self):
        return str(self.section)


class ThreeOptionsTest(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    question= HTMLField(max_length=400, null=True, blank=True)
    a = models.CharField(max_length=400, null=True, blank=True)
    b = models.CharField(max_length=400, null=True, blank=True)
    c = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Three Options Type Test"
    def __str__(self):
        return str(self.section)


class TestCategory(models.Model):
    selectTest = models.CharField(max_length=400, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Define Type Of Test"
    def __str__(self):
        return str(self.selectTest)

class ResultTitle(models.Model):
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)            
    mainHeading = models.CharField(null=True, blank=True, max_length=400)
    title = models.CharField(null=True, blank=True, max_length=400)
    discription = HTMLField(null=True, blank=True)
    point = models.CharField(null=True, blank=True, max_length=400)
    pointDiscription = HTMLField(null=True, blank=True)
    the_json = jsonfield.JSONField()

    class Meta:
        verbose_name_plural = "Add Report Title"
    # def save(self, *args, **kwargs):
    #     the_json = {}
    #     op = ResultTitle.objects.filter(className = self.className, classSection = self.classSection)
    #     if op:
    #         for i in op:
    #             json = i.the_json
    #             the_json = json
    #         the_json[self.point] = self.pointDiscription
    #         ResultTitle.objects.filter(id = i.id).update(the_json = the_json, point = '')
    #         return 
    #     else:
    #         the_json[self.point] = self.pointDiscription
    #         self.the_json = the_json
    #         self.point = ''
    #         super(ResultTitle, self).save(*args, **kwargs)
    def __str__(self):
        return str(f"{self.className} - {self.classSection}")



class AddTest(models.Model):
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    title = models.ForeignKey(Title,on_delete=CASCADE,max_length=400, null=True, blank=True)
    selectNumber = models.ForeignKey(SelectNumber,on_delete=CASCADE,max_length=400, null=True, blank=True)
    resultTitle = models.ForeignKey(ResultTitle,on_delete=CASCADE,max_length=400, null=True, blank=True)
    createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    class Meta:
        verbose_name_plural = "Add Test"
    def __str__(self):
        return str(f"{self.className} - {self.classSection}")


class Reports(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    Class = models.CharField(null=True, blank=True, max_length=200)
    classSection = models.CharField(max_length=400, null=True, blank=True)                    
    section = models.CharField(null=True, blank=True, max_length=200)
    sectionInterest = models.CharField(max_length=400, null=True, blank=True)
    # question = models.CharField(null=True, blank=True, max_length=200)
    interpretatio = models.ForeignKey(Interpretation,on_delete=CASCADE, max_length=500, null=True, blank=True)
    grade = models.CharField(null=True, blank=True, max_length=100)
    totalCount = models.FloatField(null=True, blank=True)
    # CreateAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    # industry_Grade = models.CharField(null=True, blank=True, max_length=200)
    typeOftest = models.CharField(null=True, blank=True, max_length=200)
    totalNoQu = models.FloatField(null=True, blank=True, max_length=200)
    index = models.IntegerField(null=True, blank=True)
    carrer = models.ForeignKey(Career,on_delete=CASCADE, max_length=500, null=True, blank=True)

    def __str__(self):
        return str(f"{self.user} - {self.Class} - {self.classSection}")


class TestBackupOneQuizeCorrect(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                        
    oneQuizeCorrect = models.ForeignKey(OneOptionsTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    testDiscription = models.ForeignKey(AddTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    userClickObj = models.CharField(null=True, blank=True, max_length=400)
    # createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    lastTime = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=400)
    def __str__(self):
        return str(f"{self.user} - {self.className} - {self.classSection}")


class TestBackupOneImageQuizeCorrect(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                        
    imageOneQuizeCorrect = models.ForeignKey(ImageOptionsTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    testDiscription = models.ForeignKey(AddTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    userClickObj = models.CharField(null=True, blank=True, max_length=400)
    # createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    lastTime = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=400)
    def __str__(self):
        return str(f"{self.user} - {self.className} - {self.classSection}")

class TestBackupMultipalQuize(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                        
    multipalQuize = models.ForeignKey(OptionsTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    testDiscription = models.ForeignKey(AddTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    userClickObj = models.CharField(null=True, blank=True, max_length=400)
    # createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    lastTime = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=400)
    def __str__(self):
        return str(f"{self.user} - {self.className} - {self.classSection}")

class TestBackupFiveQuize(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                        
    fiveQuize = models.ForeignKey(FiveOptionsTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    testDiscription = models.ForeignKey(AddTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    userClickObj = models.CharField(null=True, blank=True, max_length=400)
    # createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    lastTime = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=400)
    def __str__(self):
        return str(f"{self.user} - {self.className} - {self.classSection}")

class TestBackupThreeQuize(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE, max_length=100, null=True, blank=True)
    typeOfTest = models.ForeignKey(TestCategory,on_delete=CASCADE,max_length=400, null=True, blank=True)
    className = models.ForeignKey(NewClass,on_delete=CASCADE,max_length=400, null=True, blank=True)
    classSection = models.ForeignKey(AddClassSection,on_delete=CASCADE,max_length=400, null=True, blank=True)                        
    threeQuize = models.ForeignKey(ThreeOptionsTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    testDiscription = models.ForeignKey(AddTest,on_delete=CASCADE,max_length=400, null=True, blank=True)
    userClickObj = models.CharField(null=True, blank=True, max_length=400)
    # createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    lastTime = models.CharField(null=True, blank=True, max_length=100)
    number = models.CharField(null=True, blank=True, max_length=400)
    def __str__(self):
        return str(f"{self.user} - {self.className} - {self.classSection}")


class PaymentHistory(models.Model):
    user = models.ForeignKey(User,on_delete=CASCADE,max_length=400, null=True, blank=True)
    typeOfTest = models.CharField(max_length=400, null=True, blank=True)
    Class = models.CharField(max_length=400, null=True, blank=True)
    classSection = models.CharField(max_length=400, null=True, blank=True)                    
    ORDER_ID = models.CharField(max_length=400, null=True, blank=True)
    TXN_AMOUNT = models.CharField(max_length=400, null=True, blank=True)
    email = models.CharField(max_length=400, null=True, blank=True)
    status = models.CharField(max_length=400, null=True, blank=True)
    gateway = models.CharField(max_length=400, null=True, blank=True)
    bankname = models.CharField(max_length=400, null=True, blank=True)
    TXNID = models.CharField(max_length=400, null=True, blank=True)
    TXNDATE = models.CharField(max_length=400, null=True, blank=True)
    paymentCount = models.CharField(max_length=400, null=True, blank=True)
    RESPCODE = models.CharField(max_length=400, null=True, blank=True)
    CURRENCY = models.CharField(max_length=400, null=True, blank=True)
    PAYMENTMODE = models.CharField(max_length=400, null=True, blank=True)
    MID = models.CharField(max_length=400, null=True, blank=True)
    createAt = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return str(f"{self.user} - {self.Class} - {self.classSection}" )

class CarrerDescription(models.Model):
    carrer = models.ForeignKey(Career,on_delete=CASCADE,max_length=400, null=True, blank=True)
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    description = models.TextField(null=True, blank=True)