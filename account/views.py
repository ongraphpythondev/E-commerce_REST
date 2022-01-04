from django.shortcuts import render , redirect
from rest_framework import permissions
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from knox.views import LoginView as KnoxLoginView , LogoutView
from knox.auth import TokenAuthentication
from knox.models import AuthToken




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


class Login(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

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

        # login(request , user)
        user.is_verified  =True
        user.is_active = True
        user.save()
        
        return Response({
            "token": AuthToken.objects.create(user)[1],
            'user_id': user.pk,
            "mobile no.": user.mobile
            }, status=status.HTTP_201_CREATED)
        


class Verify(APIView):
    def post(self, request):
        # getting otp
        otp = request.data["otp"]
        mobile = request.data["mobile"]

        user = CustomUser.objects.filter(mobile=mobile).first()
        if user:
            data = Otp.objects.filter(user = user , otp = otp).filter()
            if data:
                user.is_verified  =True
                user.is_active = True
                user.save()
                return Response({
                    "token": AuthToken.objects.create(user)[1],
                    'user_id': user.pk,
                    "mobile no.": user.mobile
                    }, status=status.HTTP_201_CREATED)
        
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



class Logout(LogoutView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return super().post(request , format=None)



class Profile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self , request):
        serializer = ProfileSerializer(request.user)
        return Response({"user":serializer.data},status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ProfileSerializer(request.user , data = request.data , partial = True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status":"User profile updated "},  status=status.HTTP_201_CREATED)


