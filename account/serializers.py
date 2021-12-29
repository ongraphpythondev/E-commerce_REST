from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile','username']

    # def create(self, validated_data):
    #     mobile = validated_data["mobile"]
    #     user = CustomUser.objects.filter(mobile = mobile).first()
    #     if user:
    #         if user.is_verified:
    #             return "user"
    #     return CustomUser.objects.create(**validated_data)


    # velidation 
    def validate(self, data):

        # checking mobile no. is of 10 digit
        if len(str(data["mobile"])) != 10:
            raise serializers.ValidationError("Enter correct mobile number")

        
        if len(data["username"]) > 30 and len(data["username"]) < 4 :
            raise serializers.ValidationError("Enter Proper name")
            
        return data

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