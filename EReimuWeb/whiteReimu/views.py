from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from .exceptions import *
import re
from mahjong.record.reader import from_url, log_id_from_url
# Create your views here.

def uploadURL(request):
    request.encoding = 'utf-8'
    try:
        if 'logURL' not in request.GET:
            raise URLerror('Empty URL')
        URL = request.GET['logURL']
        if not re.match(r'^http://tenhou\.net/\d/\?log=.*$',URL):
            raise URLerror("Wrong URL Format")
        record = from_url(URL, 10)
        userList=[]
        usernameList=[]
        for i in record.players:
            userList.append(str(i))
            usernameList.append(i.name)
    except:
        return HttpResponse("fail")
    return render_to_response('SelectUser.html',{'userList':userList,'usernameList':usernameList,'URL':URL})

@csrf_exempt
def uploadUsername(request):
    return HttpResponse(request.POST['select_value']+request.POST['logURL'])

def uploadURLForm(request):
    return render_to_response('InputURL.html')
