from django.db.models.query import QuerySet
from rest_framework import serializers
from .models import *



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField( read_only = True )
    feedback = serializers.SlugRelatedField(read_only=True , many = True , slug_field="message")
    created_by = serializers.StringRelatedField(read_only=True )

    class Meta:
        model = Product
        fields = ["price", "name" , "image","specification","stock","available","discount","created_by","category" , "feedback" ]



    # velidation 
    # def validate(self, data):

    #     # checking mobile no. is of 10 digit
    #     if len(str(data["mobile"])) != 10:
    #         raise serializers.ValidationError("Enter correct mobile number")

        
    #     if len(data["username"]) > 30 and len(data["username"]) < 4 :
    #         raise serializers.ValidationError("Enter Proper name")
            
    #     return data

# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['mobile']

#     # velidation 
#     def validate(self, data):

#         # checking mobile no. is of 10 digit
#         if len(str(data["mobile"])) != 10:
#             raise serializers.ValidationError("Enter correct mobile number")
            
#         return data