from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from users_app.models import User
from .serializers import CalendarSerializer, EventSerializer, ImageSerializer, MonthsSerializer, EventsHistorySerializer, ResultSerializer
from .models import Calendar, Event, EventsHistory, HoursResult, Image, Months
from datetime import datetime


ENG = {
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

PL = {
        '01': 'styczeń',
        '02': 'luty',
        '03': 'marzec',
        '04': 'kwiecień',
        '05': 'maj',
        '06': 'czerwiec',
        '07': 'lipiec',
        '08': 'sierpień',
        '09': 'wrzesień',
        '10': 'październik',
        '11': 'listopad',
        '12': 'grudzień',
    }

RU = {
        '01': 'Январь',
        '02': 'Февраль',
        '03': 'Март',
        '04': 'Апрель',
        '05': 'Май',
        '06': 'Июнь',
        '07': 'Июль',
        '08': 'Август',
        '09': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь',
    }

UA = {
        '01': 'січень',
        '02': 'лютий',
        '03': 'березень',
        '04': 'квітень',
        '05': 'травень',
        '06': 'червень',
        '07': 'липень',
        '08': 'серпень',
        '09': 'вересень',
        '10': 'жовтень',
        '11': 'листопад',
        '12': 'грудень',
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
        # event=data['event'],
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
        # user__id=user_pk,
        )
    serializer = EventSerializer(instance=event, data=data, partial=True)
    # serializer = EventSerializer(event, many=False)
    if serializer.is_valid():
        serializer.save()
    evento = Event.objects.get(id=ev_pk)
    # serializero = EventSerializer(evento, many=False)
    response = Response()
    response.data = {
                'data': serializer.data,
                # 'evento': serializero.data,
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
def getRecordedMonthResults(request, user_pk, lng, studies):
    month_result = Months.objects.create()
    month_result.save()
    events = Event.objects.filter(user__id=user_pk)
    lang = f'lng_{lng}'
    print(lang)

    for ev in events:
        eventsHistory = EventsHistory.objects.create(month_id=month_result.id)
        eventsHistory.date = ev.date
        eventsHistory.event = ev.event
        eventsHistory.hours = ev.hours
        eventsHistory.minutes = ev.minutes
        eventsHistory.visits = ev.visits
        eventsHistory.publications = ev.publications
        eventsHistory.films = ev.films
        eventsHistory.studies = studies
        eventsHistory.user = ev.user
        eventsHistory.save()

        if lng == 'ENG':
            month_result.date = str(f'{str(ev.date)[0:4]} {ENG[str(ev.date)[5:7]]}')
        if lng == 'PL':
            month_result.date = str(f'{str(ev.date)[0:4]} {PL[str(ev.date)[5:7]]}')
        if lng == 'RU':
            month_result.date = str(f'{str(ev.date)[0:4]} {RU[str(ev.date)[5:7]]}')
        if lng == 'UA':
            month_result.date = str(f'{str(ev.date)[0:4]} {UA[str(ev.date)[5:7]]}')
        month_result.hours += ev.hours
        month_result.minutes += ev.minutes
        if month_result.minutes >= 60:
            month_result.hours += 1
            month_result.minutes -= 60
        month_result.visits += ev.visits
        month_result.publications += ev.publications
        month_result.films += ev.films
        month_result.studies = studies
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
    events = Event.objects.filter(user__id=user_pk)
    serializer = MonthsSerializer(results, many=True)
    all_hours = 0
    all_minutes = 0
    all_visits = 0
    all_publications = 0
    all_films = 0
    all_studies = 0
    months = []
    hours = []
    visits = []
    publications = []
    films = []
    studies = []
    for i in results:
        all_hours += i.hours
        all_minutes += i.minutes
        if all_minutes >= 60:
            all_hours += 1
            all_minutes -= 60
        all_visits += i.visits
        all_publications += i.publications
        all_films += i.films
        # all_studies = i.studies[0]
        months.append(i.date[5:])
        hours.append(i.hours)
        visits.append(i.visits)
        publications.append(i.publications)
        films.append(i.films)
        studies.append(i.studies)
    for j in events:
        all_hours += j.hours
        all_minutes += j.minutes
        if all_minutes >= 60:
            all_hours += 1
            all_minutes -= 60
        all_visits += j.visits
        all_publications += j.publications
        all_films += j.films
        all_studies = j.studies
    response = Response()
    response.data = {
        'status': status.HTTP_200_OK,
        'data': serializer.data,
        'all_hours': all_hours,
        'all_minutes': all_minutes,
        'all_visits': all_visits,
        'all_publications': all_publications,
        'all_films': all_films,
        'all_studies': all_studies,
        'months': months,
        'hours': hours,
        'visits': visits,
        'publications': publications,
        'films': films,
        'studies': studies,
    }
    return response


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


@api_view(['GET'])
def getAllCalendarDates(request):
    congregation='Sława'
    calendars = Calendar.objects.filter(congregation=congregation).exclude(action='MinistryWith')
    serializer = CalendarSerializer(
        calendars, 
        many=True,
        )
    response = Response()
    response.data = {
        'message': 'Success',
        'status': status.HTTP_200_OK,
        'data': serializer.data,
    }
    return response    


@api_view(['POST'])
def setCalendar(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    calendar = Calendar.objects.create(
        date=data['date'],
        action=data['action'],
        congregation=data['congregation'],
        groupe=data['groupe'],
        icon=data['icon'],
        # topic=data['topic'],
        user=user,
        )
    username = user.username
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        username,
        status=status.HTTP_200_OK,
        )  


@api_view(['POST'])
def getCalendarDatesByDate(request):
    data = request.data
    calendars = Calendar.objects.filter(
        date=data['date'],
        action=data['action'],
        congregation=data['congregation'],
    )
    serializer = CalendarSerializer(
        calendars, 
        many=True,
        )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        ) 


@api_view(['POST'])
def setCalendarPerson(request, pk):
    user = User.objects.get(id=pk)
    data = request.data
    calendar = Calendar.objects.create(
        date = data['date'],
        action = data['action'],
        person = data['person'],
        congregation = data['congregation'],
        time = data['time'],
        user = user,
        )
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )

@api_view(['POST'])
def setCalendarFromPerson(request, username):
    data = request.data
    user = User.objects.get(username=username)
    person = User.objects.get(id=data['person'])
    calendar = Calendar.objects.create(
        date = data['date'],
        action = data['action'],
        person = person,
        congregation = data['congregation'],
        time = data['time'],
        user = user,
        )
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )

@api_view(['POST'])
def setCalendarStand(request, username):
    data = request.data
    user = User.objects.get(username=username)
    calendar = Calendar.objects.create(
        date = data['date'],
        action = data['action'],
        person = data['person'],
        place = data['place'],
        icon = data['icon'],
        congregation = data['congregation'],
        time = data['time'],
        user = user,
        )
    stand = calendar.action[6:]
    serializer = CalendarSerializer(calendar, many=False) 
    return Response(
        serializer.data,
        stand=stand,
        status=status.HTTP_200_OK,
        )

@api_view(['POST'])
def getCalendarDatesByPerson(request):
    data = request.data
    calendars = Calendar.objects.filter(
        date=data['date'],
        action=data['action'],
    )
    serializer = CalendarSerializer(
        calendars, 
        many=True,
        )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )

@api_view(['DELETE'])
def deleteCalendar(request, pk):
    calendars = Calendar.objects.get(
        id=pk
        )
    calendars.delete()
    return Response(
        'Action was deleted',
        status=status.HTTP_200_OK,
        )     


@api_view(['GET'])
def getCalendarDatesByUser(request, pk):
    user = User.objects.get(id=pk)
    calendars = Calendar.objects.filter(
        user=user,
        )
    serializer = CalendarSerializer(
        calendars, 
        many=True,
        )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        ) 


@api_view(['POST'])
def setCalendarSpeach(request):
    data = request.data
    calendar = Calendar.objects.create(
        date=data['date'],
        action=data['action'],
        person=data['person'],
        topic=data['topic'],
        congregation=data['congregation'],
        icon=data['icon'],
        )
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )