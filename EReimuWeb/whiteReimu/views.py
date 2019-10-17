import re

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    a = Queue.objects.filter(log_url=logURL, player_name=playerName)
    b = MahjongRecord.objects.filter(log_url=logURL, player_name=playerName)
    if len(a) != 0 or len(b) != 0:
        return render_to_response('InputURL.html', {'ERRMSG': "Record Already Exist"})
    place = len(Queue.objects.all())
    if place > 50:
        return render_to_response('Queue.html', {'queryfull': 1})
    c = Queue(log_url=logURL, player_name=playerName)
    c.save()
    taskID = c.id
    time = round((place+1) * stat.averageTime / 6) / 10
    return render_to_response('Queue.html',
                              {'taskID': taskID, 'time': time, 'place': place, 'URL': logURL, 'username': playerName})


def uploadURLForm(request):
    return render_to_response('InputURL.html')


def record(request):
    content_list = MahjongRecord.objects.all()
    paginator = Paginator(content_list, 25)

    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'Record.html', {'content': content})
def failList(request):
    content_list = Fails.objects.all()
    paginator = Paginator(content_list, 25)

    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'FailList.html', {'content': content})

def checkUser(request):
    playerName = request.GET['username']
    if playerName=='Noname':
        content_list=[]
    else:
        content_list = MahjongRecord.objects.filter(player_name=playerName)
    paginator = Paginator(content_list, 25)

    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    return render(request, 'Record.html', {'content': content})

def queryList(request):
    queue = Queue.objects.all()

    return render(request, 'QueryList.html', {'content': queue,'num':len(queue)})