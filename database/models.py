from __future__ import unicode_literals
from django.db import models
from .utils import IntegerRangeField
import json
from django.core.validators import MaxValueValidator, MinValueValidator

class School(models.Model):
    name = models.CharField(max_length = 300, blank = False)
    established_date = models.DateTimeField('Establishment Date')
    school_id = models.IntegerField(max_length=20)
    def __str__(self):
        return self.name
    
    def get_date():
        return self.established_date

    def get_id():
        return self.school_id

    def json(self):
        response_data = {}
        response_data['name'] = self.name
        response_data['established_date'] = self.established_date
        response_data['school_id'] = self.school_id
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class Teacher(models.Model):
    teacher_name = models.CharField(max_length = 200, blank = False)
    appointed_date = models.DateTimeField('appointed date', blank = False)

    def __str__(self):
        return self.teacher_name

    def recently_appointed(self):
        return self.appointed_date >=  timezone.now() - datetime.timedelta(days = 30)
    
    def json(self):
        response_data = {}
        response_data['teacher_name'] = self.teacher_name
        response_data['appointed_date'] = self.appointed_date
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        

class Standard(models.Model):

    STANDARD_CHOICES = (
    ("I", "I"),
    ("II", "II"),
    ("III", "III"),
    ("IV", "IV"),
    ("V", "V"),
    ("VI", "VI"),
    ("VII", "VII"),
    ("VIII", "VIII"),
    ("IX", "IX"),
    ("X", "X"),
    ("XI", "XI"),
    ("XII", "XII"),
    )

    div = models.CharField(max_length = 5, choices = STANDARD_CHOICES, blank = False)
    class_teacher = models.ForeignKey(Teacher, on_delete= models.CASCADE)
    school = models.ForeignKey(School, on_delete= models.CASCADE)

    def __str__(self):
        return self.div

    def get_class_teacher(self):
        return self.class_teacher

    def json(self):
        response_data = {}
        response_data['div'] = self.div
        response_data['class_teacher'] = self.class_teacher
        response_data['school'] = self.school
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class Student(models.Model):
    first_name = models.CharField(max_length = 100, blank = False)
    student_id = models.IntegerField(max_length= 15, blank = False)
    last_name = models.CharField(max_length = 50)
    father_name = models.CharField(max_length = 100, blank = True)
    standard = models.ForeignKey(Standard, on_delete= models.CASCADE)

    def __str__(self):
        return str(self.first_name + " " + self.last_name)

    def json(self):
        response_data = {}
        response_data['first_name'] = self.first_name
        response_data['last_name'] = self.last_name
        response_data['father_name'] = self.father_name
        response_data['student_id'] = self.student_id
        response_data['standard'] = self.standard
        return HttpResponse(json.dumps(response_data), content_type="application/json")

class ReportCard(models.Model):
    student = models.ForeignKey(Student)
    year = models.IntegerField(validators=[MinValueValidator(2006), MaxValueValidator(2018)])
    marks_in_maths = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_english = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_hindi = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_science = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_social = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return self.student

    def percentile(self):
        total = self.marks_in_english + self.marks_in_hindi + self.marks_in_maths + self.marks_in_science + self.marks_in_social
        percent = (total/500)*100
        return percent