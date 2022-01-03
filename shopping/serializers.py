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


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    
    # velidation 
    def validate(self, data):

        # checking stock is available or not
        product = Product.objects.filter(id = data["product"].id).first()
        if product.stock == 0:
            raise serializers.ValidationError("Item is out of stock")
        
        return data


