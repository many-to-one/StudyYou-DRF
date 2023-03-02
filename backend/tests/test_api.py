from django.urls import reverse
from ..views import *
from ..models import *
from users_app.models import User
from rest_framework.test import APITestCase
from django.utils import timezone


class EventsTestAPI(APITestCase):

    def testEventApi(self):
            self.user=User.objects.create(id=6)

            # POST
            data = {
                'date': '2023-02-03',
                'event': 'test-event',
                'hours':'1',
                'minutes': '1',
                'visits': '1',
                'publications': '1',
                'films': '1',
                'studies': '1',
                'user': self.user.id
                }
            request = self.client.post(reverse('create-event', kwargs={'pk': self.user.id}), data, format='json')
            self.assertEqual(request.status_code, status.HTTP_200_OK)
            self.assertEqual(Event.objects.get().id, 1)
            self.assertEqual(Event.objects.get().event, 'test-event')
            self.assertEqual(Event.objects.count(), 1)

            # PUT
            data_upd = {
                 'event': 'updated'
            }
            request_upd = self.client.put(reverse('update-event', kwargs={'ev_pk': 1, 'user_pk': self.user.id}), data_upd, format='json')
            self.assertEqual(request_upd.status_code, status.HTTP_200_OK)
            self.assertEqual(Event.objects.get().id, 1)
            self.assertEqual(Event.objects.get().event, 'updated')
            self.assertEqual(Event.objects.count(), 1)

            #GET
            request_get = self.client.get(reverse('event', kwargs={'ev_pk': 1, 'user_pk': self.user.id}))
            event = Event.objects.get(
                id=1,
                user__id=self.user.id 
            )
            serializer = EventSerializer(event, many=False)
            self.assertEqual(request_get.data, serializer.data)
            self.assertEqual(request_get.status_code, status.HTTP_200_OK)

            #GET ALL
            request_get_all = self.client.get(reverse('events', kwargs={'pk': self.user.id}))
            events = Event.objects.filter(user__id=self.user.id)
            serializer = EventSerializer(events, many=True)
            self.assertEqual(request_get_all.data, serializer.data)
            self.assertEqual(request_get_all.status_code, status.HTTP_200_OK)
            self.assertEqual(Event.objects.count(), 1)

            #DELETE
            request_del = self.client.delete(reverse('delete-event', kwargs={'ev_pk': 1, 'user_pk': self.user.id}))
            self.assertEqual(request_del.data, 'Event was deleted')


    def testResultApi(self):
            self.user=User.objects.create(id=7)
            self.eve = Event.objects.create(
                date = datetime.now(),
                event='test-event',
                hours=1,
                minutes=30,
                visits=1,
                publications=1,
                films=1,
                studies=1,
                user=self.user
            )
            self.events = Event.objects.filter(user__id=self.user.id)
            self.result = HoursResult.objects.create(id=1)
            for h in self.events:
              self.result.date = str(h.date)[5:7]
              self.result.hours += h.hours
              self.result.minutes += h.minutes
              if self.result.minutes >= 60:
                  self.result.hours += 1
                  self.result.minutes -= 60
              self.result.visits += h.visits
              self.result.publications += h.publications
              self.result.films += h.films 
            request = self.client.get(reverse('results', kwargs={'user_pk': self.user.id}))  
            serializer = ResultSerializer(self.result, many=False)
            self.assertEqual(request.status_code, status.HTTP_200_OK)
            self.assertEqual(request.data, serializer.data)
            self.assertEqual(self.result.hours, 1)
            self.assertEqual(self.result.minutes, 30)



    def testMonthsResultsApi(self):
            
            #CREATE
            self.user=User.objects.create(id=7)
            self.month_result = Months.objects.create()
            self.month_result.save()
        
            self.eve = Event.objects.create(
                date = '2023-02-23',
                event='test-event',
                hours=1,
                minutes=30,
                visits=1,
                publications=1,
                films=1,
                studies=1,
                user=self.user
            )
            self.eve2 = Event.objects.create(
                date = '2023-02-23',
                event='test-event-2',
                hours=2,
                minutes=40,
                visits=1,
                publications=1,
                films=1,
                studies=1,
                user=self.user
            )
            self.evnts = Event.objects.filter(user=self.user.id)
            self.assertEqual(Event.objects.count(), 2)
            self.assertEqual(self.eve.event, 'test-event')
            self.assertEqual(self.eve2.event, 'test-event-2')
            self.assertEqual(self.eve.user.id, 7)
            self.assertEqual(self.eve2.user.id, 7)
            self.assertEqual(self.evnts.count(), 2)

            for ev in self.evnts:
                self.eventsHistory = EventsHistory.objects.create(month_id=self.month_result.id)
                self.eventsHistory.date = ev.date
                self.eventsHistory.event = ev.event
                self.eventsHistory.hours = ev.hours
                self.eventsHistory.minutes = ev.minutes
                self.eventsHistory.visits = ev.visits
                self.eventsHistory.publications = ev.publications
                self.eventsHistory.films = ev.films
                self.eventsHistory.user = ev.user
                self.eventsHistory.save()

                self.month_result.hours += ev.hours
                self.month_result.minutes += ev.minutes
                if self.month_result.minutes >= 60:
                    self.month_result.hours += 1
                    self.month_result.minutes -= 60
                self.month_result.visits += ev.visits
                self.month_result.publications += ev.publications
                self.month_result.films += ev.films
                self.month_result.user = ev.user

            self.assertEqual(EventsHistory.objects.count(), 2)
            self.assertEqual(self.eventsHistory.event, 'test-event-2')
            self.assertEqual(self.eventsHistory.hours, 2)

            self.month_result.save()
            self.evnts.delete()
            self.assertEqual(self.month_result.hours, 4)
            self.assertEqual(self.month_result.minutes, 10)
            self.assertEqual(Event.objects.count(), 0)

            #DELETE
            request_del = self.client.delete(reverse('delete_month_results', kwargs={'month_pk': self.month_result.pk, 'user_pk': self.user.id}))
            self.assertEqual(request_del.status_code, status.HTTP_200_OK)
            self.assertEqual(request_del.data, 'Events were deleted')

            #GET
            request_get = self.client.get(reverse('get_month_results', kwargs={'user_pk': self.user.id}))
            results = Months.objects.filter(user__id=self.user.id)
            serializer = MonthsSerializer(results, many=True)
            self.assertEqual(request_get.status_code, status.HTTP_200_OK)
            self.assertEqual(request_get.data, serializer.data)

            #GET
            request_get = self.client.get(reverse('events_history', kwargs={'user_pk': self.user.id}))
            results = EventsHistory.objects.filter(user__id=self.user.id)
            serializer = EventsHistorySerializer(results, many=True)
            self.assertEqual(request_get.status_code, status.HTTP_200_OK)
            self.assertEqual(request_get.data, serializer.data)



    def testCalendarApi(self):
        self.user = User.objects.create(id=7)
        data = {
             'date': '2023-03-02',
             'action': 'test_action',
             'user': self.user.id
        }

        #POST
        request = self.client.post(reverse('set_calendar', kwargs={'pk': self.user.id}), data, format='json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(Calendar.objects.get().id, 1)
        self.assertEqual(Calendar.objects.get().action, 'test_action')
        self.assertEqual(Calendar.objects.count(), 1)

        #GET ALL
        request_all = self.client.get(reverse('get_calendars'))
        calendars = Calendar.objects.all()
        serializer = CalendarSerializer(calendars, many=True)
        self.assertEqual(request_all.status_code, status.HTTP_200_OK)
        # self.assertEqual(request.data, serializer.data)
        self.assertEqual(Calendar.objects.get().id, 1)
        self.assertEqual(Calendar.objects.get().action, 'test_action')
        self.assertEqual(Calendar.objects.count(), 1)

        #GET
        request_get = self.client.post(reverse('get_calendar_date'), data, format='json')
        self.calendars = Calendar.objects.get(
            date='2023-03-02',
        )
        serializer = CalendarSerializer(
            calendars, 
            many=True,
        )
        self.assertEqual(request_get.status_code, status.HTTP_200_OK)
        self.assertEqual(request_get.data, serializer.data)
        self.assertEqual(self.calendars.action, 'test_action')

        #GET
        request_by_user = self.client.get(reverse('get_calendar_user', kwargs={'pk': self.user.id}))
        self.calendar = Calendar.objects.get(
            date='2023-03-02',
        )
        serializer = CalendarSerializer(
            calendars, 
            many=True,
        )
        self.assertEqual(request_by_user.status_code, status.HTTP_200_OK)
        self.assertEqual(request_by_user.data, serializer.data)
        self.assertEqual(self.calendar.action, 'test_action')

        #DELETE
        request_del = self.client.delete(reverse('delete_calendar', kwargs={'pk': self.calendar.id}))
        self.assertEqual(request_del.status_code, status.HTTP_200_OK)
        self.assertEqual(request_del.data, 'Action was deleted')
