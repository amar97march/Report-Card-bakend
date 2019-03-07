from __future__ import unicode_literals
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import School, Teacher, Standard, Student, ReportCard
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date
from .graphs import yearlyGraph, progressGraph



# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class SchoolApi(APIView):
    
    
    def post(self,request):

        params = json.loads(request.body)
    
        school = [i.json() for i in School.objects.filter(school_id = params['school_id'])]
        if not school:
            try:
                school = School(name = params['name'], established_date = params['established_date'], school_id = params['school_id'], address = params['address'],principal = params['principal'])
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
                teacher = Teacher(teacher_name = params['teacher_name'], domain = params['domain'],appointed_date = params['appointed_date'],gender = params['gender'], school = school)
                teacher.save()
                teacher = Teacher.objects.get(teacher_name = params['teacher_name'], domain = params['domain'],appointed_date = params['appointed_date'],gender = params['gender'], school = school)
                
                return HttpResponse('Staff id '+str(teacher.staff_id)+' created')

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
                reportCard = ReportCard.objects.get(student = student, year = params['year'])
                return HttpResponse('Report card already made')
            except:    
                try:
                    reportCard = ReportCard(student = student, year = params['year'], remarks = params['remarks'], marks_in_maths = params['maths'], marks_in_english = params['english'], marks_in_hindi = params['hindi'], marks_in_science = params['science'], marks_in_social = params['social'])
                    reportCard.save()
                    #Graph saving
                    marks = [reportCard.marks_in_maths, reportCard.marks_in_english, reportCard.marks_in_hindi, reportCard.marks_in_science, reportCard.marks_in_social]
                    plt1 = yearlyGraph(marks)
                    
                    plt1.savefig('media/'+str(params['student_id'])+str(params['year'])+'.jpg',transparent = True,dpi = 300) 
                    plt1.clf()
                    #progress Graph saving
                    reportCard1 = ReportCard.objects.filter(student = student).order_by('year')
                    data = [[],[],[],[],[]]
                    year = []
                    print('here2')
                    for i in reportCard1:
                        year.append(str(i.student.standard) + ' ' + str(i.year))
                        data[0].append(i.marks_in_maths)
                        data[1].append(i.marks_in_english)
                        data[2].append(i.marks_in_hindi)
                        data[3].append(i.marks_in_science)
                        data[4].append(i.marks_in_social)
                    
                    plt2, art = progressGraph(data,year)
                    print('bf')
                    plt2.savefig('media/'+str(params['student_id'])+'.jpg',transparent = True,dpi = 300,additional_artists=art,
        bbox_inches="tight") 
                    
                    response_data = reportCard.json()
                    return HttpResponse(json.dumps(response_data), content_type="application/json")
                
                except:
                    return HttpResponse('Report Card not made')
        except:
            return HttpResponse('Student id invalid')

    def get(self,request, student_id, year):
        try:
            student = Student.objects.get(student_id = student_id)
            try:
                print(str(student_id)+ ' ' +str(year))
                reportCard = ReportCard.objects.get(student = student, year = year)
                print('sf')
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

                #acedmic Graph saving
                marks = [reportCard.marks_in_maths, reportCard.marks_in_english, reportCard.marks_in_hindi, reportCard.marks_in_science, reportCard.marks_in_social]
                plt1 = yearlyGraph(marks)
                plt1.savefig('media/'+student_id+year+'.jpg',transparent = True,dpi = 300)
                plt.clf()
                #progress Graph saving
                reportCard1 = ReportCard.objects.filter(student = student)
                
                data = [[],[],[],[],[]]
                year = []

                for i in reportCard1:
                    year.append(i.student.standard + ' ' + i.year)
                    data[0].append(i.marks_in_maths)
                    data[1].append(i.marks_in_english)
                    data[2].append(i.marks_in_hindi)
                    data[3].append(i.marks_in_science)
                    data[4].append(i.marks_in_social)

                
                plt2, art = progressGraph(data,year)
                
                plt2.savefig('media/'+str(params['student_id'])+'.jpg',transparent = True,dpi = 300,additional_artists=art,
    bbox_inches="tight") 

                return HttpResponse('Changes made')
            except:
                return HttpResponse('Report card not there')
        except:
            return HttpResponse('Student id invalid')

        

        

    def delete(self, request):
        params = json.loads(request.body)

        try:
            student = Student.objects.get(student_id = params['student_id'])
            try:
                reportCard = ReportCard.objects.get(student = student, year = params['year'])
                reportCard.delete()
                return HttpResponse(str(student) + "'s " + str(params['year']) + " report card deleted")
            except:
                return HttpResponse('Report card not there')
        except:
            return HttpResponse('Student id invalid')

class graphApi(APIView):

    def get(self,request, student_id):
        try:
            student = Student.objects.get(student_id = student_id)
            try:
                reportCard = ReportCard.objects.filter(student = student)
            
                data = []
                year = []
                for i in reportCard:
                    year.append(i.year)
                    temp = []
                    temp.extend([i.marks_in_maths,i.marks_in_english,i.marks_in_hindi,i.marks_in_science,i.marks_in_social])
                    data.append(temp)
                plt, art = progressGraph(data,year)
                
                plt.savefig('media/'+student_id+'.jpg',transparent = True,dpi = 300,additional_artists=art,
    bbox_inches="tight") 
                
                
            
            except:
                return HttpResponse('Report card not there')
        except:
            HttpResponse('Student id invalid')