from rest_framework import serializers
from .models import *


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile']

    # velidation 
    def validate(self, data):

        # checking mobile no. is of 10 digit
        if len(str(data["mobile"])) != 10:
            raise serializers.ValidationError("Enter correct mobile number")
            
        return data


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"

    # velidation 
    def validate(self, data):

        # checking mobile no. is of 10 digit
        if len(str(data["mobile"])) != 10:
            raise serializers.ValidationError("Enter correct mobile number")
        
        
        if len(data["otp"]) != 4:
            raise serializers.ValidationError("Enter correct otp")
            
        return data


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    # velidation 
    def validate(self, data):

        # validation
        if data.get("username") and (len(data["username"]) > 30 or len(data["username"]) < 3):
            raise serializers.ValidationError("Enter proper username")
        if data.get("email") and (len(data["email"]) > 50 or len(data["username"]) < 5):
            raise serializers.ValidationError("Enter proper email")
        if data.get("address") and len(data["address"]) > 500:
            raise serializers.ValidationError("Address must be less then 500")
        if  data.get("first_name") and len(data.get("first_name")) > 30 :
            raise serializers.ValidationError("Enter proper first name")
        if data.get("last_name") and len(data["last_name"]) > 30 :
            raise serializers.ValidationError("Enter proper last name")
        

        return data