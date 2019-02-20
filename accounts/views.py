from __future__ import unicode_literals
from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.http import HttpResponse
from django.core.exceptions import MultipleObjectsReturned
from django.core.serializers.json import DjangoJSONEncoder
from .models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt


# Create your views here

@csrf_exempt
class signUp(APIView):

    @csrf_exempt
    def post(request):
        params = json.loads(request.body)


        avataar = request.data['avataar']
        #email, user_type, first_name, last_name, date_joined, is_active,_avataar
        user = User.objects.filter(email = params['email'])
        if not user:
            user = User(email = params['email'],password = params['password'],first_name = params['user_type'],last_name = params['last_name'], avataar = avataar)
            token, _ = Token.objects.get_or_create(user = user)
            return Response({'token': token.key},status = HTTP_200_OK)
        else:
            return HttpResponse('User already exist')

    @csrf_exempt
    def get(request):
        params = json.loads(request.body)

        try:
            user = User.objects.get(email = params['email'],password = params['password'])
        except User.DoesNotExist:
            HttpResponse('user not exist')  

        

        
    