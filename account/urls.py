from django.urls import path 
from .views import *

urlpatterns = [
    path('verify', Verify.as_view() ),
    path('resend_otp', ResendOTP.as_view() ),
    path('login', Login.as_view() ),
    path('logout', Logout.as_view() ),
]