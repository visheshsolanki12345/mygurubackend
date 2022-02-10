from django.db import models
from django.db.models.deletion import CASCADE
import jsonfield

# Create your models here.


RIGHT_ANS_CHOICES =(
    ("Interest", "Interest"),
)

class Section(models.Model):
    typeOfSection = models.CharField(choices = RIGHT_ANS_CHOICES,null=True, blank=True, max_length=300)
    section = models.CharField(max_length=400, null=True, blank=True)
    timeDuration = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return str(f"{self.typeOfSection} - {self.section}")

class InterpretationGrade(models.Model):
    grade = models.CharField(max_length=400,null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Grades Name"
    def __str__(self):
        return str(self.grade)

class ShowGrade(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    selectGrade = models.ForeignKey(InterpretationGrade,on_delete=CASCADE,max_length=400, null=True, blank=True)
    score = models.CharField(max_length=400, null=True, blank=True)
    the_json = jsonfield.JSONField()
    class Meta:
        verbose_name_plural = "Add Grades Marking"
    def save(self, *args, **kwargs):
        the_json = {}
        op = ShowGrade.objects.filter(section = self.section)
        if op:
            for i in op:
                json = i.the_json
                the_json = json
                the_json[str(self.selectGrade)] = self.score
            ShowGrade.objects.filter(id = i.id).update(the_json = the_json)
            return ShowGrade
        else:
            the_json[str(self.selectGrade)] = self.score
            self.the_json = the_json
            super(ShowGrade, self).save(*args, **kwargs)
    def __str__(self):
        return str(f"{self.section}")

class Interpretation(models.Model):    
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
        op = Interpretation.objects.filter(section = self.section, grade=self.grade)
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
            Interpretation.objects.filter(id = i.id).update(the_json = the_json, the_title = the_title)
            return Interpretation
        else:
            the_json[str(self.selectGrade)] = self.point
            the_title[str(self.selectGrade)] = self.title
            self.the_json = the_json
            self.the_title = the_title
            super(Interpretation, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.section)

class SelectNumber(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    numberEachQuestion  = models.FloatField(null=True, blank=True)
    class Meta:
        verbose_name_plural = "Add Options Marking in each Questions"
    def __str__(self):
        return str(self.section)

RIGHT_ANS_CHOICES =(
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
)

class AddQuestion(models.Model):
    section = models.ForeignKey(Section,on_delete=CASCADE,max_length=400, null=True, blank=True)
    questionText = models.TextField(null=True, blank=True)
    question= models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    a = models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    aText = models.TextField(null=True, blank=True)
    b = models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    bText = models.TextField(null=True, blank=True)
    c = models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    cText = models.TextField(null=True, blank=True)
    d = models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    dText = models.TextField(null=True, blank=True)
    e = models.ImageField(upload_to = 'Image-Interest', null=True, blank=True, max_length=200)
    eText = models.TextField(null=True, blank=True)
    rightAns = models.CharField(choices = RIGHT_ANS_CHOICES,null=True, blank=True, max_length=300)

    def save(self, *args, **kwargs):
        if self.rightAns == 'A':
            self.rightAns = self.a
        elif self.rightAns == 'B':
            self.rightAns = self.b
        elif self.rightAns == 'C':
            self.rightAns = self.c
        elif self.rightAns == 'D':
            self.rightAns = self.d
        elif self.rightAns == 'E':
            self.rightAns = self.e
        super(AddQuestion, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.section)
