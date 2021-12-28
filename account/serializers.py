from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__' 

    # creating user
    def create(self, validated_data):


        user = CustomUser.objects.create(
            mobile=validated_data['mobile'],
            otp=validated_data['otp'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    # velidation 
    def validate(self, data):

        # checking mobile no. is of 10 digit
        if len(str(data["mobile"])) != 10:
            raise serializers.ValidationError("Enter correct mobile number")
        return data