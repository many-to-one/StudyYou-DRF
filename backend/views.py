from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users_app.models import User
from users_app.utils import Util
from .serializers import CalendarSerializer, EventSerializer, ImageSerializer, MonthsSerializer, EventsHistorySerializer, PlacesStandSerializer, ResultSerializer
from .models import Calendar, Event, EventsHistory, HoursResult, Image, Months, PlacesStand
from datetime import datetime
from random import sample
import pandas as pd


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
        )
    serializer = EventSerializer(instance=event, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    response = Response()
    response.data = {
            'data': serializer.data,
            'status': status.HTTP_205_RESET_CONTENT
        }
    return response


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
    serializer = ResultSerializer(result, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
def getRecordedMonthResults(request, user_pk, lng, studies, month):

    data = request.data
    hours_ = ''
    minutes_ = ''
    publications_ = ''
    films_ = ''
    visits_ = ''
    studies_ = ''
    report_ = ''
    from_ = ''
    regards_ = ''

    user = User.objects.get(id=user_pk)
    report_user = User.objects.get(report=True)
    month_result = Months.objects.create()
    month_result.save()
    events = Event.objects.filter(user__id=user_pk)

    for ev in events:
        eventsHistory = EventsHistory.objects.create(month_id=month_result.id)
        eventsHistory.date = ev.date
        eventsHistory.hours = ev.hours
        eventsHistory.minutes = ev.minutes
        eventsHistory.visits = ev.visits
        eventsHistory.publications = ev.publications
        eventsHistory.films = int(data['films'])
        eventsHistory.studies = studies
        eventsHistory.user = ev.user
        eventsHistory.save()

        if lng == 'ENG':
            hours_ = 'Hours:'
            minutes_ = 'Minutes:'
            publications_ = 'Publications:'
            films_ = 'Films:'
            visits_ = 'Visits:'
            studies_ = 'Studies:'
            month_ = 'Month:'
            report_ = 'Report:'
            from_ = 'From:'
            regards_ = 'Kind regards,'

        if lng == 'PL':
            hours_ = 'Godziny:'
            minutes_ = 'Minuty:'
            publications_ = 'Publikacje:'
            films_ = 'Filmy:'
            visits_ = 'Odwiedziny:'
            studies_ = 'Studia:'
            month_ = 'Miesiąc:'
            report_ = 'Owoc'
            from_ = 'za'
            regards_ = 'Pozdrawiam,'

        if lng == 'RU':
            hours_ = 'Часы:'
            minutes_ = 'Минуты:'
            publications_ = 'Публикации:'
            films_ = 'Фильмы:'
            visits_ = 'Посещения:'
            studies_ = 'Изучения:'
            month_ = 'Месяц:'
            report_ = 'Отчет'
            from_ = 'за'
            regards_ = 'С уважением'

        if lng == 'UA':
            hours_ = 'Години:'
            publications_ = 'Публікації:'
            minutes_ = 'Хвилини:'
            films_ = 'Фільми:'
            visits_ = 'Відвідування:'
            studies_ = 'Вивчення:'
            month_ = 'Мiсяц:'
            report_ = 'Звіт'
            from_ = 'за'
            regards_ = 'З повагою,'

        month_result.date = f'{month} {str(ev.date)[0:4]}'
        month_result.hours += ev.hours
        month_result.minutes += ev.minutes
        if month_result.minutes >= 60:
            month_result.hours += 1
            month_result.minutes -= 60
        month_result.visits += ev.visits
        month_result.publications += ev.publications
        month_result.films += int(data['films'])
        month_result.studies = studies
        month_result.user = ev.user
    month_result.save()
    events.delete()
    serializer = MonthsSerializer(month_result, many=False)
    email_body = f'{month_} {month_result.date}\n \n {hours_} {month_result.hours}\n {minutes_} {month_result.minutes}\n {publications_} {month_result.publications} \n {visits_} {month_result.visits} \n {films_} {month_result.films} \n {studies_} {month_result.studies} \n \n {regards_} \n {user.username}'
    data = {'email_body': email_body, 
            'to_email': report_user.email,
            'email_subject': f'{report_} {user.username} {from_} {month_result.date}'}

    Util.send_email(data)      
    return Response(
        serializer.data,
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


@api_view(['DELETE'])
def deleteAllMonthsResults(request, user_pk):
    history = EventsHistory.objects.filter(
        user__id=user_pk,
        )[12:]
    months = Months.objects.filter(
        user__id=user_pk
    )[12:]
    EventsHistory.objects.exclude(pk__in=history).delete()
    Months.objects.exclude(pk__in=months).delete()
    # history.delete()
    # months.delete()
    print(f'################## {history} ###################')
    print(f'################## {months} ###################')

    return Response(
        'Events were deleted',
        status=status.HTTP_200_OK,
        )
    

@api_view(['GET'])
def getMonthsResults(request, user_pk):
    results = Months.objects.filter(user__id=user_pk)
    bar_chart = Months.objects.filter(user__id=user_pk).order_by('-id')
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
    for i in bar_chart:
        months.append(i.date[:-4])
        hours.append(i.hours)
        visits.append(i.visits)
        publications.append(i.publications)
        films.append(i.films)
        studies.append(i.studies)
    for i in results:
        all_hours += i.hours
        all_minutes += i.minutes
        if all_minutes >= 60:
            all_hours += 1
            all_minutes -= 60
        all_visits += i.visits
        all_publications += i.publications
        all_films += i.films
        all_studies = i.studies
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
        'months': months[:4],
        'hours': hours[:4],
        'visits': visits[:4],
        'publications': publications[:4],
        'films': films[:4],
        'studies': studies[:4],
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
def setCalendar(request, pk, week_ago):
    user = User.objects.get(id=pk)
    data = request.data
    user.action = data['action']
    user.save()
    users = User.objects.filter(
        groupe=data['groupe']
    )
    check_calendar = Calendar.objects.filter(
        date=week_ago,
        action=data['action'],
        user=user,
    )
    check_same_date = Calendar.objects.filter(
        date=data['date'],
        user=user
    )
    arr_check = []
    for check in check_same_date:
        arr_check.append(check.icon)
    for check in check_calendar:
        arr_check.append(check.icon)
    if check_calendar:
        calendar = Calendar.objects.create(
            date=data['date'],
            time='user week ago', # duplicate date for iteration of sorted Timetable-list in React
            arr_icon=arr_check,
            check_arr_icon=True,
            action=data['action'],
            congregation=data['congregation'],
            groupe=data['groupe'],
            # icon=data['icon'],
            user=user,
            )
    elif check_same_date:
        calendar = Calendar.objects.create(
            date=data['date'],
            time=data['date'], # duplicate date for iteration of sorted Timetable-list in React
            arr_icon=arr_check,
            check_arr_icon=True,
            action=data['action'],
            congregation=data['congregation'],
            groupe=data['groupe'],
            icon=data['icon'],
            user=user,
            )
    elif check_calendar and check_same_date:
        calendar = Calendar.objects.create(
            date=data['date'],
            time='user week ago', # duplicate date for iteration of sorted Timetable-list in React
            arr_icon=arr_check,
            check_arr_icon=True,
            action=data['action'],
            congregation=data['congregation'],
            groupe=data['groupe'],
            icon=data['icon'],
            user=user,
            )
    elif data['action'] == 'Cleaning':
        for user in users:
            calendar = Calendar.objects.create(
                date=data['date'],
                time=data['date'], # duplicate date for iteration of sorted Timetable-list in React
                action=data['action'],
                congregation=data['congregation'],
                groupe=data['groupe'],
                icon=data['icon'],
                user=user,
            )
    elif not check_calendar and not check_same_date:
        calendar = Calendar.objects.create(
            date=data['date'],
            time=data['date'], # duplicate date for iteration of sorted Timetable-list in React
            action=data['action'],
            congregation=data['congregation'],
            groupe=data['groupe'],
            icon=data['icon'],
            user=user,
            )
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
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
        time = data['date'],
        at_time = data['at_time'],
        icon = data['icon'],
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
        time = data['date'],
        at_time = data['at_time'],
        icon = data['icon'],
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
    user.action = data['action'],
    user.save()
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

@api_view(['PUT'])
def updateCalendarStand(request, pk):
    data = request.data
    calendar = Calendar.objects.get(id=pk)
    calendar.user = User.objects.get(username=data['user'])
    calendar.person = data['person']
    calendar.save()
    serializer = CalendarSerializer(instance=calendar, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
    response = Response()
    response.data = {
            'data': serializer.data,
            'status': status.HTTP_205_RESET_CONTENT
        }
    return response

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


@api_view(['POST'])
def setCalendarSpeachFromList(request, pk):
    data = request.data
    user = User.objects.get(id=pk)
    calendar = Calendar.objects.create(
        date=data['date'],
        action=data['action'],
        topic=data['topic'],
        congregation=data['congregation'],
        icon=data['icon'],
        user=user
        )
    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )


@api_view(['POST', 'GET', 'DELETE'])
def setPlacesStand(request, congregation):
    if request.method == "POST":
        data = request.data
        place = PlacesStand.objects.create(
            name=data['name'],
            congregation=congregation
        )
        serializer = PlacesStandSerializer(place, many=False)
        response = Response()
        response.data = {
            'message': 'Success',
            'status': status.HTTP_200_OK,
            'data': serializer.data,
        }
        return response  
    elif request.method == "GET":
        places = PlacesStand.objects.filter(
            congregation=congregation,
        )
        serializer = PlacesStandSerializer(places, many=True)
        response = Response()
        response.data = {
            'message': 'Success',
            'status': status.HTTP_200_OK,
            'data': serializer.data,
        }
        return response
    elif request.method == "DELETE":
        data = request.data
        place = PlacesStand.objects.filter(
            name=data['name'],
            congregation=congregation,
        )
        place.delete()
        response = Response()
        response.data = {
            'message': 'Deleted successfully',
            'status': status.HTTP_404_NOT_FOUND,
        }
        return response


@api_view(['POST', 'GET', 'DELETE']) 
def setRandomStand(request, congregation, date, count, dw):
    if request.method == 'POST':
        data = request.data
        users = User.objects.filter(
            congregation=congregation,
            stand=True,
        )
        udl = []
        for a in users:
            udl.append(a.id)
        ud = sample(udl, len(udl))


        if dw == 'Tue':
            time = [f'{date} 10:00', f'{date} 11:00', f'{date} 12:00', f'{date} 13:00']
            place = ['Park przy zamku']
            for i in range(4):
                print(f'##############{i}#############')
                user1 = User.objects.get(id=ud[i])
                user2 = User.objects.get(id=ud[i+2])
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user1,
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user1,
                    )
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user2,
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user2,
                    )


        elif dw == 'Thu':
            time = [f'{date} 10:00', f'{date} 11:00', f'{date} 16:00', f'{date} 17:00']
            place = ['Skrzużowanie Centrum', 'Skrzużowanie Centrum', 'Wjazd do Galerii', 'Wjazd do Galerii']
            for i in range(4):
                print(f'##############{i}#############')
                user1 = User.objects.get(id=ud[i])
                user2 = User.objects.get(id=ud[i+2])
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user1,
                    place = place[i],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user1,
                    )
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user2,
                    place = place[i],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user2,
                    )


        elif dw == 'Fri':
            time = [f'{date} 10:00', f'{date} 11:00', f'{date} 16:00', f'{date} 17:00']
            place = ['Park przy zamku', 'Park przy zamku', 'Wjazd do Galerii', 'Wjazd do Galerii']
            for i in range(4):
                print(f'##############{i}#############')
                user1 = User.objects.get(id=ud[i])
                user2 = User.objects.get(id=ud[i+2])
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user1,
                    place = place[i],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user1,
                    )
                calendar = Calendar.objects.create(
                    date = date,
                    action = data['action'],
                    person = user2,
                    place = place[i],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time[i],
                    user = user2,
                    )
                

        else:
            return Response(
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )