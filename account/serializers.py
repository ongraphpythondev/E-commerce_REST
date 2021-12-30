from rest_framework import serializers
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['mobile','username']

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