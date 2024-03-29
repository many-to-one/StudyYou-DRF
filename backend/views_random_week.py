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
def setRandomWeek(request):   
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
        school_leaders = User.objects.filter(
            congregation=data['congregation'],
            school_leader=True,
        )
        prayers = User.objects.filter(
            congregation=data['congregation'],
            helper=True,
        )
        icons = [
            'md-shield',
            'albums',
            'md-film-outline',
            'md-file-tray-full',
            'md-library',
        ]
        action = [
            'SpiritualGems',
            'TreasuresFromGodsWord',
            'Discussion',
            'LocalNeeds',
            'BibleStudyLeader',
        ]
        li = []
        le = []
        sl = []
        pr = []
        for a in leaders:
            li.append(a.username)
        lid = sample(li, len(li))
        for a in lectors:
            le.append(a.username)
        lec = sample(le, len(le))
        for a in school_leaders:
            sl.append(a.username)
        sle = sample(sl, len(sl))
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

        lecth = len(lec)
        sleth = len(sle)
        preth = len(pre)
        i = 0
        for day in date:
            for i in range(5):
                calendar = Calendar.objects.create(
                    date=day,
                    time=day,
                    action = action[i],
                    icon=icons[i],
                    congregation=data['congregation'],
                    user = User.objects.get(username=lid[i]),
                )
            lid = sample(li, len(li))

            lecth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'BibleStudyLector',
                icon='md-reader',
                congregation=data['congregation'],
                user = User.objects.get(username=lec[lecth]),
            )
            if lecth == 0:
                lecth = len(lec)

            preth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'FirstPrayer',
                icon='ios-layers',
                congregation=data['congregation'],
                user = User.objects.get(username=pre[preth]),
            )
            pre = sample(pr, len(pr))
            preth = len(pre)
            preth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'LastPrayer',
                icon='ios-layers',
                congregation=data['congregation'],
                user = User.objects.get(username=pre[preth]),
            )
            if preth == 0:
                preth = len(pre)

            sleth -= 1
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'SchoolLeader',
                icon='school-sharp',
                congregation=data['congregation'],
                user = User.objects.get(username=sle[sleth]),
            )
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'LeaderAndIntroductoryRemarks',
                icon='person-outline',
                congregation=data['congregation'],
                user = User.objects.get(username=sle[sleth]),
            )
            if sleth == 0:
                sleth = len(sle)

        serializer = CalendarSerializer(
        calendar, 
        many=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            )