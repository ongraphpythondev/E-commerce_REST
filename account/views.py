from django.shortcuts import render , redirect
from twilio.rest import Client
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from django.contrib.auth import login , logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication



import random
import string
# Create your views here.


# sending message to client
# account_sid = os.environ.get("account_sid") 
# auth_token = os.environ.get("auth_token") 
# client = Client(account_sid, auth_token)

def generate_otp(mobile_no ):
    try:
        
        otp=""
        for i in range(4):
            otp+=str(random.randint(1,9))

        # message = client.messages \
        #     .create(
        #         body=f'Its from Ongraph your code is {otp}',
        #         from_='+17817904373',
        #         to='+91'+mobile_no
        # )
        return otp
    except: 
        return "NOT OK"


# class Register(APIView):
#     def post(self, request):
        
#         mobile = request.data["mobile"]
#         user = CustomUser.objects.filter(mobile = mobile).first()
#         if user:
#             if user.is_verified:
#                 return Response({"status":"User has already account"}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 otp = generate_otp(mobile)
#                 if otp == "NOT OK" :
#                     return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
#                 serializer = OTPSerializer(data = )

#                 return Response({"status":"OTP sended to mobile please verify"}, status=status.HTTP_201_CREATED)
#         serializer = RegisterSerializer(data = request.data)
#         if serializer.is_valid():
            
#             otp = generate_otp(request.data["mobile"] )
            
#             if otp == "NOT OK" :
#                 return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
#             request.session['otp'] = otp
#             request.session['mobile'] = request.data["mobile"]
#             serializer.save()


#             return Response({"data":serializer.data , "status":"OTP sended to mobile please verify"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Verify(APIView):
    def post(self, request):
        # getting otp
        otp = request.data["otp"]
        mobile = request.data["mobile"]

        user = CustomUser.objects.filter(mobile=mobile).first()
        if user:
            data = Otp.objects.filter(user = user , otp = otp).filter()
            if data:
                token , created = Token.objects.get_or_create(user=user)
                user.is_verified  =True
                user.is_active = True
                user.save()
                return Response({
                    'token': token.key,
                    'user_id': user.pk
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error":"Please enter correct otp"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"User not found"}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTP(APIView):
    def post(self, request):
        mobile = request.data["mobile"]
        # validation
        if not mobile or len(str(mobile)) != 10:
            return Response({"error":"please enter mobile no."}, status=status.HTTP_400_BAD_REQUEST)
        
        otp = generate_otp(mobile)
        
        if otp == "NOT OK" :
            return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
        user = CustomUser.objects.filter(mobile = mobile).first()
        if user:
            otpobj = Otp.objects.filter(user = user).first()
            otpobj.otp = otp
            otpobj.save()
            return Response({"status":f"{otp} OTP resended to mobile please verify"}, status=status.HTTP_200_OK)
        else:
            return Response({"status":"user not found"}, status=status.HTTP_200_OK)




class Login(APIView):
    def post(self, request):
        
        # getting data
        mobile = request.data["mobile"]

        # user object
        user = CustomUser.objects.filter(mobile = mobile).first()
        if not user:
            serializer = LoginSerializer(data = request.data)
            if serializer.is_valid():
                
                otp = generate_otp(request.data["mobile"] )
                
                if otp == "NOT OK" :
                    return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer.save()

                user = CustomUser.objects.filter(mobile = mobile).first()
                otpobj = Otp.objects.create(user = user , otp = otp)
                otpobj.save()


                return Response({"data":serializer.data , "status":f"{otp}OTP sended to mobile please verify"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # checking that no. is verified or not
        if not user.is_verified:
            return Response({"error":"User not verify please verify it"}, status=status.HTTP_400_BAD_REQUEST)

        # checking that no. is active 
        # if user.is_active:
            # login(request , user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
            }, status=status.HTTP_200_OK)
        
        # if user is not active so user must enter otp for it
        otp = generate_otp(mobile)
        if otp == "NOT OK" :
            return Response({"status":"something went wrong please try again"}, status=status.HTTP_400_BAD_REQUEST)
            
        # setting session
        return Response({"otp":f"{otp} sended to your mobile phone"}, status=status.HTTP_400_BAD_REQUEST)



class Logout( APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


