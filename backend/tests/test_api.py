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