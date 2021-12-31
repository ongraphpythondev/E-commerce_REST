from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('product', Product)
router.register('category', Category)
router.register('feedback', Feedback)

urlpatterns = [
    path('', include(router.urls)),
    
]