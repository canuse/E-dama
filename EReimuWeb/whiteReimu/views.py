from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from whiteReimu.models import *
from .exceptions import *
import re
from mahjong.record.reader import from_url, log_id_from_url
# Create your views here.
class Process:
    status=False

def uploadURL(request):
    request.encoding = 'utf-8'
    try:
        if 'logURL' not in request.GET:
            raise EmptyForm
        URL = request.GET['logURL']
        if not re.match(r'^http://tenhou\.net/\d/\?log=.*$',URL):
            raise URLError
        record = from_url(URL, 10)
        userList=[]
        usernameList=[]
        for i in record.players:
            userList.append(str(i))
            usernameList.append(i.name)
    except URLError as e:
        return render_to_response('InputURL.html',{'ERRMSG':"Wrong URL Format"})
    except EmptyForm as e:
        return render_to_response('InputURL.html',{'ERRMSG':"Missing items in Form"})
    except Exception as e:
        return render_to_response('InputURL.html',{'ERRMSG':"Cann't find the record"})
    return render(request,'InputURL.html',{'userList':userList,'usernameList':usernameList,'URL':URL})


def uploadUsername(request):
    logURL=request.POST['logURL']
    playerName=request.POST['playerName']
    a=Queue.objects.filter(log_url=request.POST['logURL'],player_name=playerName)
    if len(a)!=0:
        return HttpResponse("already exist")
    c=Queue(log_url=request.POST['logURL'],player_name=playerName)
    c.save()
    Process.status=not Process.status
    return HttpResponse(request.POST['playerName']+request.POST['logURL']+str(Process.status))

def uploadURLForm(request):
    return render_to_response('InputURL.html')
