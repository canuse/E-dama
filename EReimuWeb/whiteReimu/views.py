import re

from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from mahjong.record.reader import from_url

from whiteReimu.models import *
from .exceptions import *
from .scheduler import *

# Create your views here.


def uploadURL(request):
    request.encoding = 'utf-8'
    try:
        if 'logURL' not in request.GET:
            raise EmptyForm
        URL = request.GET['logURL']
        if not re.match(r'^http://tenhou\.net/\d/\?log=.*$', URL):
            raise URLError
        record = from_url(URL, 10)
        userList = []
        usernameList = []
        for i in record.players:
            userList.append(str(i))
            usernameList.append(i.name)
    except URLError as e:
        return render_to_response('InputURL.html', {'ERRMSG': "Wrong URL Format"})
    except EmptyForm as e:
        return render_to_response('InputURL.html', {'ERRMSG': "Missing items in Form"})
    except Exception as e:
        return render_to_response('InputURL.html', {'ERRMSG': "Cann't find the record"})
    return render(request, 'InputURL.html', {'userList': userList, 'usernameList': usernameList, 'URL': URL})


def uploadUsername(request):
    logURL = request.POST['logURL']
    playerName = request.POST['playerName']
    # query record in database to confirm no repeat
    a = Queue.objects.filter(log_url=request.POST['logURL'], player_name=playerName)
    b = MahjongRecord.objects.filter(log_url=request.POST['logURL'], player_name=playerName)
    if len(a) != 0 or len(b) != 0:
        return render_to_response('InputURL.html', {'ERRMSG': "Record Already Exist"})
    c = Queue(log_url=logURL, player_name=playerName)
    c.save()
    return HttpResponse(request.POST['playerName'] + request.POST['logURL'] + str(Process.status))


def uploadURLForm(request):
    return render_to_response('InputURL.html')
