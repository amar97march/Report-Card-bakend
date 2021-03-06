from __future__ import unicode_literals
from django.db import models
from .utils import IntegerRangeField
import json
from django.utils import timezone
from datetime import datetime, date, timedelta
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
import dateutil.parser

class School(models.Model):
    name = models.CharField(max_length = 300, blank = False)
    principal = models.CharField(max_length = 300, default = 'Not provided')
    established_date = models.DateField('Establishment Date')
    address = models.CharField(max_length = 500, default = 'Not provided')
    school_id = models.CharField(unique = True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    def __str__(self):
        return self.name

    def get_date(self):
        return self.established_date

    def get_id(self):
        return self.school_id

    def json(self):
        response_data = {}
        response_data['name'] = self.name
        response_data['principal'] = self.principal
        response_data['established_date'] = str(self.established_date)
        response_data['school_id'] = self.school_id
        response_data['address'] = self.address
        return response_data

class Teacher(models.Model):

    GENDER = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
    )

    teacher_name = models.CharField(max_length = 200, blank = False)
    staff_id = models.IntegerField(primary_key = True)
    domain = models.CharField(max_length = 300, default = 'Not provided')
    appointed_date = models.DateField('appointed date', blank = False)
    gender = models.CharField(max_length = 2, choices = GENDER, null = True)
    school = models.ForeignKey(School, on_delete= models.CASCADE, null = True)

    def exp(self):
        exp = date.today() - self.appointed_date
        return exp.days/365
    
    def __str__(self):
        return self.teacher_name

    def recently_appointed(self):
        return self.appointed_date >=  date.today() - timedelta(days = 30)
    
    def json(self):
        response_data = {}
        response_data['teacher_name'] = self.teacher_name
        response_data['staff_id'] = self.staff_id
        response_data['domain'] = self.domain
        response_data['appointed_date'] = str(self.appointed_date)
        response_data['recently_appointed'] = self.recently_appointed()
        response_data['exp'] = self.exp()
        response_data['gender'] = self.gender
        return response_data
        

class Standard(models.Model):

    STANDARD_CHOICES = (
    (1, "I"),
    (2, "II"),
    (3, "III"),
    (4, "IV"),
    (5, "V"),
    (6, "VI"),
    (7, "VII"),
    (8, "VIII"),
    (9, "IX"),
    (10, "X"),
    (1, "XI"),
    (12, "XII")
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
        response_data['class_teacher'] = str(self.class_teacher)
        response_data['school'] = str(self.school)
        return response_data

class Student(models.Model):
    first_name = models.CharField(max_length = 100, blank = False)
    student_id = models.IntegerField(blank = False)
    last_name = models.CharField(max_length = 50)
    dob = models.DateField(max_length = 8, null = True)
    father_name = models.CharField(max_length = 100, blank = True)
    standard = models.ForeignKey(Standard, on_delete= models.CASCADE)
    address = models.CharField(max_length = 500, default = 'Not provided')

    def __str__(self):
        return str(self.first_name + " " + self.last_name)



    def age(self):
        return relativedelta(date.today(), self.dob)

    def json(self):
        response_data = {}
        response_data['first_name'] = self.first_name
        response_data['last_name'] = self.last_name
        response_data['father_name'] = self.father_name
        #response_data['age'] = self.age()
        response_data['student_id'] = self.student_id
        response_data['standard'] = str(self.standard)
        response_data['address'] = self.address
        return response_data

class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    year = models.IntegerField(validators=[MinValueValidator(2006), MaxValueValidator(2018)])
    remarks = models.CharField(max_length = 300,blank = True)
    marks_in_maths = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_english = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_hindi = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_science = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    marks_in_social = models.IntegerField(default= -1, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return str(str(self.student) + ' - Class:'+str(self.student.standard) + ' ' + str(self.year))

    def percentile(self):
        total = self.marks_in_english + self.marks_in_hindi + self.marks_in_maths + self.marks_in_science + self.marks_in_social
        percent = (total/500)*100
        return percent

    def json(self):
        response_data = {}
        response_data['student'] = str(self.student)
        response_data['year'] = self.year
        response_data['standard'] = str(self.student.standard)
        response_data['remarks'] = self.remarks
        response_data['maths'] = self.marks_in_maths
        response_data['english'] = self.marks_in_english
        response_data['hindi'] = self.marks_in_hindi
        response_data['science'] = self.marks_in_science
        response_data['social'] = self.marks_in_social
        response_data['percentage'] = self.percentile()
        response_data['acedmicGraph'] = '/media/'+str(self.student.student_id)+str(self.year)+'.jpg'
        response_data['progressGraph'] = '/media/'+str(self.student.student_id)+'.jpg'
        return response_data