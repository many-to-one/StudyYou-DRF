from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users_app.models import User
from .serializers import CalendarSerializer, EventSerializer, ImageSerializer, MonthsSerializer, EventsHistorySerializer, ResultSerializer
from .models import Calendar, Event, EventsHistory, HoursResult, Image, Months
from datetime import datetime


month_list_UA = {
        '01': 'January',
        '02': 'February',
        '03': 'March',
        '04': 'April',
        '05': 'May',
        '06': 'June',
        '07': 'July',
        '08': 'August',
        '09': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }

@api_view(['GET'])
def getEvents(request, pk):
    events = Event.objects.filter(user__id=pk).order_by('-date')
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def getEventsHistory(request, pk):
#     events = Event.objects.filter(user__id=pk).order_by('-date')
#     serializer = EventSerializer(events, many=True)
#     return Response(serializer.data)    

@api_view(['GET'])
def getEvent(request, ev_pk, user_pk):
    event = Event.objects.get(
        id=ev_pk,
        user__id=user_pk,
        )
    serializer = EventSerializer(event, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getEventHistory(request, user_pk):
    event = EventsHistory.objects.filter(user=user_pk)
    serializer = EventsHistorySerializer(event, many=True)
    return Response(serializer.data)    

@api_view(['POST'])
def createEvent(request, pk):
    new_user = User.objects.get(id=pk)
    data = request.data
    event = Event.objects.create(
        # date=data['date'][5:7],
        event=data['event'],
        hours=data['hours'],
        minutes=data['minutes'],
        visits=data['visits'],
        publications=data['publications'],
        films=data['films'],
        user=new_user
    )
    print(request.user)
    serializer = EventSerializer(event, many=False)
    response = Response()
    response.data = {
        'message': 'Success',
        'status': status.HTTP_200_OK,
        'data': serializer.data,
    }
    return response  

@api_view(['PUT'])
def updateEvent(request, ev_pk, user_pk):
    data = request.data
    event = Event.objects.get(
        id=ev_pk,
        user__id=user_pk,
        )
    serializer = EventSerializer(instance=event, data=data)
    if serializer.is_valid():
        serializer.save()
    evento = Event.objects.get(id=ev_pk)
    serializero = EventSerializer(evento, many=False)
    response = Response()
    response.data = {
                'data': serializer.data,
                'evento': serializero.data,
                'status': status.HTTP_205_RESET_CONTENT
            }
    return response

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )

@api_view(['DELETE'])
def deleteEvent(request, ev_pk, user_pk):
    data = request.data
    event = Event.objects.get(
        id=ev_pk,
        user__id=user_pk,
        )
    event.delete()
    return Response('Event was deleted')


@api_view(['DELETE'])
def deleteAll(request, user_pk):
    events = Event.objects.filter(
        user__id=user_pk,
    )
    events.delete()
    return Response('Events were deleted')

@api_view(['GET'])
def getResults(request, user_pk):
    events = Event.objects.filter(user__id=user_pk)
    # result = HoursResult.objects.create() 
    # result.save()
    result = HoursResult.objects.get(id=1)  
    for h in events:
        result.date = str(h.date)[5:7] # result.date = month_list_UA[str(h.date)[5:7]]   
        result.hours += h.hours
        result.minutes += h.minutes
        if result.minutes >= 60:
            result.hours += 1
            result.minutes -= 60
        result.visits += h.visits
        result.publications += h.publications
        result.films += h.films 
    # result.save()
    serializer = ResultSerializer(result, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )

@api_view(['GET'])
def getRecordedMonthResults(request, user_pk):
    month_result = Months.objects.create()
    month_result.save()
    events = Event.objects.filter(user__id=user_pk)

    for ev in events:
        eventsHistory = EventsHistory.objects.create(month_id=month_result.id)
        eventsHistory.date = ev.date
        eventsHistory.event = ev.event
        eventsHistory.hours = ev.hours
        eventsHistory.minutes = ev.minutes
        eventsHistory.visits = ev.visits
        eventsHistory.publications = ev.publications
        eventsHistory.films = ev.films
        eventsHistory.user = ev.user
        eventsHistory.save()

        month_result.date = str(f'{str(ev.date)[0:4]} {month_list_UA[str(ev.date)[5:7]]}')
        month_result.hours += ev.hours
        month_result.minutes += ev.minutes
        if month_result.minutes >= 60:
            month_result.hours += 1
            month_result.minutes -= 60
        month_result.visits += ev.visits
        month_result.publications += ev.publications
        month_result.films += ev.films
        month_result.user = ev.user
    month_result.save()
    events.delete()
    serializer = MonthsSerializer(month_result, many=False)
    return Response(
        serializer.data,
        # month_result.date
        ) 

@api_view(['DELETE'])
def deleteMonthResult(request, month_pk, user_pk):
    events = Months.objects.filter(
        id=month_pk,
        user__id=user_pk,
        )
    history = EventsHistory.objects.filter(
        user__id=user_pk,
        month=month_pk,
        )
    events.delete()
    history.delete()
    return Response(
        'Events were deleted',
        status=status.HTTP_200_OK,
        )
    

@api_view(['GET'])
def getMonthsResults(request, user_pk):
    results = Months.objects.filter(user__id=user_pk)
    serializer = MonthsSerializer(results, many=True)
    # results = EventsHistory.objects.filter(user__id=user_pk)
    # serializer = EventsHistorySerializer(results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getImages(request):
    img = Image.objects.all()
    serializer = ImageSerializer(img, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getImage(request, pk):
    img = Image.objects.get(id=pk)
    serializer = ImageSerializer(img, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def setCalendarDate(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    calendar = Calendar.objects.create(
        date = data
    )
    serializer = CalendarSerializer(calendar, many=False)
    response = Response()
    response.data = {
        'message': 'Success',
        'status': status.HTTP_200_OK,
        'data': serializer.data,
    }
    return response 


@api_view(['GET'])
def getAllCalendarDates(request):
    calendars = Calendar.objects.all()
    serializer = CalendarSerializer(calendars, many=True)
    response = Response()
    response.data = {
        'message': 'Success',
        'status': status.HTTP_200_OK,
        'data': serializer.data,
    }
    return response