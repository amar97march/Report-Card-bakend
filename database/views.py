from __future__ import unicode_literals
from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers.json import DjangoJSONEncoder
from .models import School


# Create your views here.
class school(APIView):
    
    def post(self,request):

        params = json.loads(request.body)
        #name, established_date, school_id
        school = [i.json() for i in School.objects.filter(name = params['name'])]
        if not school:
            school = School(name = params['name'], established_date = params['established_date'], school_id = params['school_id'])
            return HttpResponse('School Created')
        else:
            return HttpResponse('Already Exist')

        