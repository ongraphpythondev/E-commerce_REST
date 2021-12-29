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
from django.contrib.auth import login , logout
from rest_framework.permissions import IsAuthenticated



import random
import string
# Create your views here.


# sending message to client
account_sid = os.environ.get("account_sid") 
auth_token = os.environ.get("auth_token") 
client = Client(account_sid, auth_token)

def generate_otp(mobile_no ):
    try:
        
        otp=""
        for i in range(4):
            otp+=str(random.randint(1,9))

        message = client.messages \
            .create(
                body=f'Its from Ongraph your code is {otp}',
                from_='+17817904373',
                to='+91'+mobile_no
        )
        return otp
    except: 
        return "NOT OK"


class Register(APIView):
    def post(self, request):
        
        mobile = request.data["mobile"]
        user = CustomUser.objects.filter(mobile = mobile).first()
        if user:
            if user.is_verified:
                return Response({"status":"User has already account"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                otp = generate_otp(mobile)
                if otp == "NOT OK" :
                    return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
                request.session['otp'] = otp
                request.session['mobile'] = request.data["mobile"]

                return Response({"status":"OTP sended to mobile please verify"}, status=status.HTTP_201_CREATED)
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            
            otp = generate_otp(request.data["mobile"] )
            
            if otp == "NOT OK" :
                return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
            request.session['otp'] = otp
            request.session['mobile'] = request.data["mobile"]
            serializer.save()


            return Response({"data":serializer.data , "status":"OTP sended to mobile please verify"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Verify(APIView):
    def post(self, request):
        # getting otp
        userotp = request.data["otp"]
        sessionotp = request.session.get("otp")
        sessionmobile = request.session.get("mobile")
        print(sessionotp , userotp , sessionmobile)

        # validation
        if not userotp:
            return Response({"error":"please enter otp"}, status=status.HTTP_400_BAD_REQUEST)
        if not sessionotp or not sessionmobile:
            return Response({"error":"please register first"}, status=status.HTTP_400_BAD_REQUEST)
        
        # User object
        user = CustomUser.objects.filter(mobile = sessionmobile).first()
        if not user:
            return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)

        # checking the otp we received and otp in db is same 
        if userotp != sessionotp :
            return Response({"error":"Please enter correct otp"}, status=status.HTTP_400_BAD_REQUEST)
        
        # user is verified and active
        user.is_verified = True
        user.is_active = True
        user.save()

        # login user
        login(request , user)

        # delete sessions
        del request.session['otp']
        del request.session['mobile']

        return Response({"success":"User succesfully verified and login"}, status=status.HTTP_200_OK)


class ResendOTP(APIView):
    def get(self, request):
        sessionmobile = request.session.get("mobile")
        # validation
        if not sessionmobile:
            return Response({"error":"please register first"}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = generate_otp(sessionmobile)
        
        if otp == "NOT OK" :
            return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
        # setting session
        request.session['otp'] = otp
        request.session['mobile'] = sessionmobile
        return Response({"status":"OTP resended to mobile please verify"}, status=status.HTTP_200_OK)



class Login(APIView):
    def post(self, request):
        
        # getting data
        mobile = request.data["mobile"]

        # validating data
        if len(mobile) != 10:
            return Response({"error":"Enter valid mobile no."}, status=status.HTTP_400_BAD_REQUEST)
            
        # user object
        user = CustomUser.objects.get(mobile = mobile)
        if not user:
            return Response({"error":"User not found please create account first"}, status=status.HTTP_400_BAD_REQUEST)

        # checking that no. is verified or not
        if not user.is_verified:
            return Response({"error":"User not verify please again register"}, status=status.HTTP_400_BAD_REQUEST)

        # checking that no. is active 
        if user.is_active:
            login(request , user)
            return Response({"status":"User logged in succesfully"}, status=status.HTTP_200_OK)
        
        # if user is not active so user must enter otp for it
        otp = generate_otp(mobile)
        if otp == "NOT OK" :
            return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
        # setting session
        request.session['otp'] = otp
        request.session['mobile'] = mobile
        return Response({"status":"Please enter OTP to login "}, status=status.HTTP_400_BAD_REQUEST)



class Logout( APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        user.is_active = False
        user.save()
        logout(request)
        return Response({"status":"User logout succesfully"}, status=status.HTTP_200_OK)


