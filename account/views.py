from django.shortcuts import render , redirect
from django.http import HttpResponse
from rest_framework.serializers import Serializer
from twilio.rest import Client
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *

import random
import string
# Create your views here.



class Login(APIView):
    def post(self, request):
        
        # get random password pf length 8 with letters, digits, and symbols
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        
        otp=""
        for i in range(4):
            otp+=str(random.randint(1,9))

        data = {
            "mobile":request.data["mobile"],
            "password" : password,
            "otp" : otp
        }
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            serializer.save()

            account_sid = os.environ.get("account_sid") 
            auth_token = os.environ.get("auth_token") 
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                    body=f'Its from Ongraph your code is {otp}',
                    from_='+17817904373',
                    to='+91'+request.data["mobile"]
                )

            print(message.sid)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Verify(APIView):
    def post(self, request , user_pk = None):
        otp = request.data["otp"]
        if user_pk == None:
            return Response({"error":"write pk"}, status=status.HTTP_400_BAD_REQUEST)
        if not otp:
            return Response({"error":"please enter otp"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(pk = user_pk)
        if not user:
            return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)

        if user.otp != otp :
            return Response({"error":"Please enter correct otp"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_verified = True
        user.save()
        return Response({"success":"User succesfully verified"}, status=status.HTTP_200_OK)
