from django.db.models.query import QuerySet
from rest_framework import serializers

from account.models import CustomUser
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
        product = Product.objects.filter(pk = data["product"].pk).first()
        if product.stock == 0:
            raise serializers.ValidationError("Item is out of stock")

        user = CustomUser.objects.filter(pk = data["user"].pk).first()
        if user.address == None:
            raise serializers.ValidationError("Please enter the address before order")

        cost = 0
        if data.get("bank"):
            bank = Bank.objects.filter(bank = data.get("bank")).first()
            if data.get("emi") == True:
                cost = product.price  * 1.2
            else:
                cost = product.price  * ( 100 - bank.discount  ) /100
        if data.get("pay_on_delivery") == True:
            cost = product.price

        # discount of 250 rs. for first time purchase
        order = user.order.all()
        print(order)
        if len(order) == 0:
            if product.price < 250:
                cost = 0
            else:
                cost = cost - 250

        
        
        data["discounted_price"] = cost
        product.stock -= 1
        product.save()
        return data


