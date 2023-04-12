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
        for a in leaders:
            li.append(a.username)
        lid = sample(li, len(li))
        for a in lectors:
            le.append(a.username)
        lec = sample(le, len(le))
        for a in school_leaders:
            sl.append(a.username)
        sle = sample(sl, len(sl))

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


            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'SpiritualGems',
            #     icon=icons[1],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[1]),
            # )
            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'TreasuresFromGodsWord',
            #     icon=icons[2],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[2]),
            # )
            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'SchoolLeader',
            #     icon=icons[3],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[3]),
            # )
            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'Discussion',
            #     icon=icons[4],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[4]),
            # )
            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'LocalNeeds',
            #     icon=icons[5],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[5]),
            # )
            # calendar = Calendar.objects.create(
            #     date=day,
            #     time=day,
            #     action = 'BibleStudyLeader',
            #     icon=icons[6],
            #     congregation=data['congregation'],
            #     user = User.objects.get(username=lid[6]),
            # )

            # lid = sample(li, len(li)) 