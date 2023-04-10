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
def setRandomService(request):   
    if request.method == 'POST':
        data = request.data
        users = User.objects.filter(
            congregation=data['congregation'],
            service=True,
        )
        icons = [
            'mic',
            'md-headset',
            'man-sharp',
        ]
        udl = []
        for a in users:
            udl.append(a.username)
        ud = sample(udl, len(udl))

        dates = data['date']
        dates += '.'
        print(f'############{dates}##############')
        date = []
        di = ''
        count = 0

        for d in dates:
            count += 1
            di += d
            if d == ',' or d == '.':
                date.append(di[:10])
                di = ''

        for day in date:
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'Microphones',
                icon=icons[0],
                congregation=data['congregation'],
                user = User.objects.get(username=ud[0]),
            )
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'Microphones',
                icon=icons[0],
                congregation=data['congregation'],
                user = User.objects.get(username=ud[1]),
            )
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'Music',
                icon=icons[1],
                congregation=data['congregation'],
                user = User.objects.get(username=ud[2]),
            )
            calendar = Calendar.objects.create(
                date=day,
                time=day,
                action = 'Duty',
                icon=icons[2],
                congregation=data['congregation'],
                user = User.objects.get(username=ud[3]),
            )
            ud = sample(udl, len(udl))
        serializer = CalendarSerializer(
        calendar, 
        many=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            ) 