from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.rest import Client
import os
# Create your views here.


@csrf_exempt
def login(request):
    if request.method == "POST":
        mobile = request.POST["mobile"]
        account_sid = os.environ.get("account_sid") 
        auth_token = os.environ.get("auth_token") 
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body='This is the ship that made the Kessel Run in fourteen parsecs?',
                from_='+17817904373',
                to='+917060699351'
            )

        print(message.sid)

    
    return HttpResponse("done")
