from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render , redirect
from rest_framework import viewsets
from django.db.models import Q  
from knox.auth import TokenAuthentication



# Create your views here.

class Products(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class Category(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class Feedback(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()





class CartList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self , request):
        cart = Cart.objects.filter(user = request.user).order_by('created_at')
        serializer = CartSerializer(cart , many = True)
        print(type(cart) , type(serializer.data))
        return Response({"cart":serializer.data} , status=status.HTTP_200_OK)



class AddCart(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request , pk):
        product = Product.objects.get(pk = pk)
        data = {
            "user": request.user.pk,
            "product" : product.pk
        }
        serializer = CartSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({"status":f"{product.name} is added to cart"} , status=status.HTTP_201_CREATED)



class OrderList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    
    def get(self , request):
        order = Order.objects.filter(user = request.user).order_by('-created_at')
        serializer = OrderSerializer(order , many = True)
        return Response({"orders":serializer.data} , status=status.HTTP_200_OK)



class Addorder(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request , pk = None):
        if pk == None:
            pass

        cart = Cart.objects.filter(pk = pk).first()
        if not cart:
            return Response({"status":f"cart not found"} , status=status.HTTP_404_NOT_FOUND)

        pay_on_delivery = False
        bank = None
        emi = False
        if request.data.get("bank") :
            bank = Bank.objects.filter(bank = request.data.get("bank")).first() 
            bank = bank.pk
            if request.data.get("emi") == "True":
                emi = True

        elif request.data.get("pay_on_delivery") == "True":
            pay_on_delivery = True
            
        else:
            return Response({"status":f"Choose at least one of them ( bank or pay on delivery )"} , status=status.HTTP_403_FORBIDDEN)

        data = {
                "user": request.user.pk,
                "product" : cart.product.pk,
                "pay_on_delivery" : pay_on_delivery,
                "bank":bank,
                "emi" : emi
            }
        serializer = OrderSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cart.delete()
        return Response({"status":f"{serializer.validated_data.get('discounted_price')} Rs. is paid from customer"} , status=status.HTTP_201_CREATED)


class FindProduct(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self , request):
        
        product_name = request.data["name"]

        products = Product.objects.filter(
            Q(name__contains = product_name)
            )
        if not products:
            return Response({"status":f"No product found"} , status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(products , many = True)
        return Response({"products":serializer.data} , status=status.HTTP_201_CREATED)


 
