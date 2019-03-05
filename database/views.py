from __future__ import unicode_literals
from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers.json import DjangoJSONEncoder
from .models import School, Teacher, Standard, Student, ReportCard
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class SchoolApi(APIView):
    
    
    def post(self,request):

        params = json.loads(request.body)
    
        school = [i.json() for i in School.objects.filter(school_id = params['school_id'])]
        if not school:
            try:
                school = School(name = params['name'], established_date = parse_date(params['established_date']), school_id = params['school_id'], address = params['address'],principal = params['principal'])
                school.save()
                response_data = school.json()
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except:
                return HttpResponse('School not created')
        else:
            return HttpResponse('Already Exist')

    
    def get(self, request, school_id, *args, **kwargs):
        
        try:
            school = School.objects.get(school_id = school_id)
            response_data = school.json()
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        except:
            return HttpResponse('school not there')

    
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

    
    def delete(self, request):
        params = json.loads(request.body)
        try:
            school = School.objects.get(school_id = params['school_id'])
        except:
            return HttpResponse('school not there')

        school.delete()

        return HttpResponse('School('+ str(params['school_id'])+ ') removed')

class TeacherApi(APIView):

    def post(self, request):
        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = params['school_id'])
        except :
            return HttpResponse('school not there')
        try:
            teacher = Teacher.objects.get(teacher_name = params['teacher_name'],domain = params['domain'], school = school)
            return HttpResponse('Teacher already present. ID- '+ str(teacher.staff_id))
        except:
            try:
                teacher = Teacher(teacher_name = params['teacher_name'], domain = params['domain'],appointed_date = parse_date(params['appointed_date']),gender = params['gender'], school = school)
                teacher.save()
                
                response_data = teacher.json()
                return HttpResponse(json.dumps(response_data), content_type="application/json")

            except:
                return HttpResponse('Teacher not created')
            
        
        

    def get(self, request, staff_id, *args, **kwargs):

        try:
            
            teacher = Teacher.objects.get(staff_id = staff_id)
            response_data = teacher.json()
            
            return HttpResponse(json.dumps(response_data), content_type="application/json")

        except:
            return HttpResponse('Teacher not there')
        
        

    def put(self, request):

        params = json.loads(request.body)

        try:
            teacher = Teacher.objects.get(staff_id = params['id'])
            teacher.domain = params['domain']
            teacher.save()
            return HttpResponse('Changes done to staff id '+ str(params['id']))
        except:
            return HttpResponse('Staff not found')

        

    def delete(self, request):

        params = json.loads(request.body)
        try:
            teacher = Teacher.objects.get(staff_id = params['id'])
            teacher.delete()
            return HttpResponse('staff id '+ str(params['id']) + ' deleted')
        except:
            return HttpResponse('Teacher not there')

        

class StandardApi(APIView):
    
    def post(self, request):

        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = params['school_id'])
            try:
                teacher = Teacher.objects.get(staff_id = params['teacher_id'])
                try :
                    standard = Standard.objects.get(div = params['div'],class_teacher = teacher,school = school)
                    return HttpResponse('Class already present')
                except:
                    try:
                        standard = Standard(div = params['div'],class_teacher = teacher, school = school)
                        standard.save()
                        response_data = standard.json()
                        return HttpResponse(json.dumps(response_data), content_type="application/json")


                    except:
                        return HttpResponse('Standard not created')
            except:
                return HttpResponse('Teacher not there')
        except:
            return HttpResponse('school not there')
        
    def get(self, request, div, *args, **kwargs):
        
        try:
            
            standard = Standard.objects.get(div = div)
            
            return HttpResponse(json.dumps(standard.json()), content_type="application/json")
        except:
            return HttpResponse('No standard exist')

        

    def delete(self, request):
        
        params = json.loads(request.body)

        try:
            school = School.objects.get(school_id = params['school_id'])
            try:
                standard = Standard.objects.get(div = params['div'], school = school)
                standard.delete()
                return HttpResponse(str(params['div']) + 'th division deleted')
            except:
                return HttpResponse('standard not there')
            
        except:
            return HttpResponse('school not there')

        

class StudentApi(APIView):

    def post(self, request):
        params = json.loads(request.body)
        
        try:
            school = School.objects.get(school_id = params['school_id'])
            try:
                standard = Standard.objects.get(div = params['div'],school=school)
                try:
                    student = Student.objects.get(student_id = params['student_id'])
                    return HttpResponse('Student already registered')
                except:
                    try:
                        params['first_name'] = 'Amar'
                        params['last_name'] = 'Singh'
                        params['dob'] = '1997-03-26'
                        params['father_name'] = 'shailesh'

                        student = Student(first_name = params['first_name'], last_name = params['last_name'],dob = parse_date(params['dob']),father_name = params['father_name'],standard = standard, address = params['address'],student_id= params['student_id'])
                        student.save()
                        print('asfaf')
                        response_data = student.json()
                        return HttpResponse(json.dumps(response_data), content_type="application/json")
                    except:
                        return HttpResponse('Student not created')
                
            except Standard.DoesNotExist:
                return HttpResponse('No standard exist')
        except:
            return HttpResponse('school not there')
        

        
        
    def get(self,request,student_id, *args, **kwargs):
        
        if int(student_id) == 0:
            print(str(student_id))
            try:
                students = [i.json() for i in Student.objects.all()]
                print('saf')
                return HttpResponse(json.dumps(students), content_type="application/json")
            except:
                return HttpResponse('No student')
        else:
            try:
                student = Student.objects.get(student_id = student_id)
                print('sfafS')
                response_data = student.json()
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except:
                return HttpResponse('Student id invalid')
        
        

    def put(self, request):

        params = json.loads(request.body)
        try:
            student = Student.objects.get(student_id = params['student_id'])
            try:
                school = School.objects.get(school_id = params['school_id'])
                try:
                    print('asf')
                    standard = Standard.objects.get(div = params['div'], school = school)
                    print('asf')
                    student.standard = standard
                    student.address = params['address']
                    student.save()
                    print('asf')
                    response_data = student.json()
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except :
                    return HttpResponse('Standard not exist')
            
            except School.DoesNotExist:
                return HttpResponse('school not there')
        except:
            return HttpResponse('Student id is invalid')

        

        

    def delete(self, request):
        params = json.loads(request.body)
        try:
            
            student = Student.objects.get(student_id = params['student_id'])
            student.delete()
            return HttpResponse(str(params['student_id']) + 'th student deleted')
        except:
            return HttpResponse('Student id invalid')

        

class ReportCardApi(APIView):

    def post(self,request):
        params = json.loads(request.body)
        
        try:
            student = Student.objects.get(student_id = params['student_id'])
            try:
                print('gg')
                reportCard = ReportCard.objects.filter(student = student, year = params['year'])
                return HttpResponse('Report card already made')
            except:    
                try:
                    reportCard = ReportCard(student = student, year = params['year'], remarks = params['remarks'], marks_in_maths = params['maths'], marks_in_english = params['english'], marks_in_hindi = params['hindi'], marks_in_science = params['science'], marks_in_social = params['social'])
                    reportCard.save()
                    print('sf')
                    response_data = reportCard.json()
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                except:
                    return HttpResponse('Report Card not made')
        except:
            HttpResponse('Student id invalid')

    def get(request, student, year):
        try:
            student = Student.objects.get(student_id = params['student_id'])
            try:
                reportCard = ReportCard.objects.get(student = student, year = params['year'])
                print('afasfg')
                response_data = reportCard.json()
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            except:
                return HttpResponse('Report card not there')
        except:
            HttpResponse('Student id invalid')


    def put(self,request):
        params = json.loads(request.body)

        try:
            student = Student.objects.get(student_id = params['student_id'])
            try:
                reportCard = ReportCard.objects.get(student = student, year = params['year'])
                reportCard.marks_in_maths = params['maths']
                reportCard.marks_in_english = params['english']
                reportCard.marks_in_hindi = params['hindi']
                reportCard.marks_in_science = params['science']
                reportCard.marks_in_social = params['social']
                reportCard.remarks = params['remarks']
                reportCard.save()

                return HttpResponse('Changes made')
            except:
                return HttpResponse('Report card not there')
        except:
            HttpResponse('Student id invalid')

        

        

    def delete(request):
        params = json.loads(request.body)

        try:
            student = Student.objects.get(student_id = params['student_id'])
        except:
            HttpResponse('Student id invalid')

        try:
            reportCard = ReportCard.objetcs.get(student = student, year = params['year'])
        except:
            return HttpResponse('Report card not there')

        reportCard.delete()
        return HttpResponse(student+"'s " + params['year'] + " report card deleted")