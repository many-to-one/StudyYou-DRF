from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users_app.models import User
from users_app.utils import Util
from .serializers import CalendarSerializer
from .models import Calendar
from random import sample
import pandas as pd
import random


@api_view(['POST', 'GET', 'DELETE']) 
def setRandomWeekend(request):   
    if request.method == 'POST':
        data = request.data
        leaders = User.objects.filter(
            congregation=data['congregation'],
            leader=True,
        )
        lectors = User.objects.filter(
            congregation=data['congregation'],
            lector=True,
        )
        prayers = User.objects.filter(
            congregation=data['congregation'],
            helper=True,
        )
        icons = [
            'person-outline',
            'person-sharp',
            'md-reader',
        ]
        action = [
            'WeekendLeader',
            'WatchTowerLeader',
            'WatchTowerLector',
        ]
        li = []
        le = []
        pr = []
        for a in leaders:
            li.append(a.username)
        lid = sample(li, len(li))

        for a in lectors:
            le.append(a.username)
        lec = sample(le, len(le))

        for a in prayers:
            pr.append(a.username)
        pre = sample(pr, len(pr))

        dates = data['date']
        dates += '.'
        date = []
        di = ''
        count = 0

        for d in dates:
            count += 1
            di += d
            if d == ',' or d == '.':
                date.append(di[:10])
                di = ''

        lidth = len(lid)
        lecth = len(lec)
        preth = len(pre)

        for day in date:
            preth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = action[0],
                icon=icons[0],
                congregation=data['congregation'],
                user = User.objects.get(username=pre[preth]),
            )
            if preth == 0:
                preth = len(pre)

            lidth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = action[1],
                icon=icons[1],
                congregation=data['congregation'],
                user = User.objects.get(username=lid[lidth]),
            )
            if lidth == 0:
                lidth = len(lid)

            lecth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = action[2],
                icon=icons[2],
                congregation=data['congregation'],
                user = User.objects.get(username=lec[lecth]),
            )
            if lecth == 0:
                lecth = len(lec)
            
        serializer = CalendarSerializer(
        calendar, 
        many=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            )