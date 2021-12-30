from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class Home(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self , request):
        products = Product.objects.all()
        serializer = ProductSerializer(products , many = True)
        return Response({"Products":serializer.data} , status=status.HTTP_200_OK)
