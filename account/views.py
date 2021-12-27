from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.rest import Client
# Create your views here.


@csrf_exempt
def login(request):
    if request.method == "POST":
        mobile = request.POST["mobile"]
        print(mobile)
        account_sid = "AC796220b91d3780f0783e40474c9dea67"
        auth_token = "2da75293af496540050556c2358ebbf5"
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body='This is the ship that made the Kessel Run in fourteen parsecs?',
                from_='+17817904373',
                to='+917060699351'
            )

        print(message.sid)

    
    return HttpResponse("done")
