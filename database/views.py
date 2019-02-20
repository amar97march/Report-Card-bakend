from __future__ import unicode_literals
from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers.json import DjangoJSONEncoder
from .models import School, Teacher, Standard, Student


# Create your views here.
class SchoolApi(APIView):
    
    def post(self,request):

        params = json.loads(request.body)
        
        school = [i.json() for i in School.objects.filter(name = params['name'])]
        if not school:
            school = School(name = params['name'], established_date = params['established_date'], school_id = params['school_id'], address = params['address'],principal = params['principal'])
            return HttpResponse('School Created')
        else:
            return HttpResponse('Already Exist')

    def get(self, request,school_id):
        
        params = json.loads(request.body)
        try:
            school = School.objects.get(school_id = school_id)
        except School.DoesNotExist:
            HttpResponse('school not there')

        response_data = school.json()

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def put(self, request):
        params = json.loads(request.body)
        try:
            school = School.objects.get(school_id = params['school_id'])
        except School.DoesNotExist:
            HttpResponse('school not there')
        
        school.name = params['name']
        school.principal = params['principal']
        school.save()

        response_data = school.json()

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def delete(self, request,school_id):
        try:
            school = School.objects.get(school_id = school_id)
        except:
            HttpResponse('school not there')

        school.delete()

        HttpResponse('School ('+ school_id+ ') removed')

class TeacherApi(APIView):

    def post(self,request,school_id):
        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = school_id)
        except School.DoesNotExist:
            HttpResponse('school not there')

        try:
            teacher = Teacher(teacher_name = params['teacher_name'], domain = params['domain'],appointed_date = params['appointed_date'],gender = params['gender'], school = school)
        except:
            HttpResponse('Teacher not created')

    def get(self, request, id):

        try:
            teacher = Teacher.objects.get(teacher_id = id)
        except:
            HttpResponse('Teacher not there')
        
        response_data = teacher.json()

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def put(self, request, id):

        params = json.loads(request.body)

        try:
            teacher = Teacher.objects.get(staff_id = id)
        except:
            HttpResponse('Staff not found')

        teacher.domain = params['domain']
        teacher.save()

    def delete(self, request,id):
        
        try:
            teacher = Teacher.objects.get(teacher_id = id)
        except:
            HttpResponse('Teacher not there')

        teacher.delete()

        HttpResponse('staff id '+ id + ' deleted')

class StandardApi(APIView):
    
    def post(self, request):

        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = school_id)
        except School.DoesNotExist:
            HttpResponse('school not there')
        
        try:
            teacher = Teacher.objects.get(teacher_id = id)
        except:
            HttpResponse('Teacher not there')
        
        try:
            standard = Standard(div = params['div'],class_teacher = teacher, school = school)
        except:
            HttpResponse('Standard not created')

        response_data = standard.json()

        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def get(self, request):
        
        try:
            standard = [i.json() for i in Standard.objects.all()]
        except Standard.DoesNotExist:
            HttpResponse('No standard exist')

        return HttpResponse(json.dumps(standard), content_type="application/json")

    def delete(self, request):
        
        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = params['school_id'])
        except School.DoesNotExist:
            HttpResponse('school not there')

        try:
            standard = Standard.objects.get(div = params[div,]school = school)
        except:
            HttpResponse('standard not there')

        standard.delete()

        HttpResponse(params['div'] + 'division deleted')

class StudentApi(APIView):

    def post(self, request):
        params = json.loads(request.body)

        try:
            standard = [i.json() for i in Standard.objects.all()]
        except Standard.DoesNotExist:
            HttpResponse('No standard exist')

        try:
            student = Student(first_name = params['first_name'], last_name = params['last_name'],dob = params['dob'],father_name = params['father_name'],standard = standard, address = params['address'])
        except:
            HttpResponse('Student not created')

        response_data = student.json()
        return HttpResponse(json.dumps(response_data), content_type="application/json")
        
    def get(self,request,id):
        
        try:
            student = Student.objects.get(student_id = id)
        except:
            HttpResponse('Student id invalid')
        
        response_data = student.json()
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def put(self, request):

        params = json.loads(request.body)

        try:
            student = Student.objects.get(student_id = params['student_id'])
        except:
            HttpResponse('Student id invalid')

        try:
            school = School.objects.get(school_id = params['school_id'])
        except School.DoesNotExist:
            HttpResponse('school not there')

        try:
            standard = Standard.objects.get(div = params['div'], school = school)
        except Standard.DoesNotExist:
            HttpResponse('No standard exist')

        student.standard = standard
        student.address = params['address']
        student.save()

        response_data = student.json()
        return HttpResponse(json.dumps(response_data), content_type="application/json")

    def delete(self, request, id):

        try:
            student = Student.objects.get(student_id = student_id)
        except:
            HttpResponse('Student id invalid')

        student.delete()
        HttpResponse(id + 'th student deleted')