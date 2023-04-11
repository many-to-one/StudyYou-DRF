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
def setRandomMinistry(request):   
    if request.method == 'POST':
        data = request.data
        users = User.objects.filter(
            congregation=data['congregation'],
            ministry_event=True,
        ).exclude(
            groupe=1,
        )
        udl = []
        for a in users:
            udl.append(a.username)
        ud = sample(udl, len(udl))

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

    length = len(ud)
    for day in date:
        length -= 1
        calendar = Calendar.objects.create(
            date=day,
            time=day,
            action = 'MinistryLeader',
            icon=data['icon'],
            congregation=data['congregation'],
            user = User.objects.get(username=ud[length]),
        )
        if length == 0:
            length = len(ud)
    serializer = CalendarSerializer(
        calendar, 
        many=False,
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        ) 