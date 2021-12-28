from django.urls import path 
from .views import *

urlpatterns = [
    path('login', Login.as_view() ),
    path('verify/<int:user_pk>', Verify.as_view() ),
]