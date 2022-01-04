from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('product', Products)
router.register('category', Category)
router.register('feedback', Feedback)

urlpatterns = [
    path('', include(router.urls)),
    path('cart', CartList.as_view() ),
    path('addcart/<int:pk>', AddCart.as_view() ),
    path('order', OrderList.as_view() ),
    path('addorder/<int:pk>', Addorder.as_view() ),
    path('addorder', Addorder.as_view() ),
    path('findproduct', FindProduct.as_view() ),
    
]