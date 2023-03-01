from django.utils import timezone
from django.test import TestCase
from ..models import *
from users_app.models import User


class EventTest(TestCase):
    def setUp(self):
        Event.objects.create(
            date = timezone.now(),
            event='test-event',
            hours='1',
            minutes='1',
            visits='1',
            publications='1',
            films='1',
            studies='1',
            user=User.objects.create(
                id=1,
            )
        )

        Event.objects.create(
            date = timezone.now(),
            event='test-event2',
            hours='2',
            minutes='2',
            visits='2',
            publications='2',
            films='2',
            studies='2',
            user=User.objects.create(
                id=2,
            )
        )

    def testEvent(self):
        Event.objects.get(date=timezone.now()) 
        Event.objects.get(event='test-event')
        Event.objects.get(hours='1')
        Event.objects.get(minutes='1')
        Event.objects.get(visits='1')
        Event.objects.get(publications='1')
        Event.objects.get(films='1')
        Event.objects.get(studies='1')   
        Event.objects.get(user=1)


class MonthTest(TestCase):
    def setUp(self):
        Months.objects.create(
            date = timezone.now(),
            hours='2',
            minutes='2',
            visits='2',
            publications='2',
            films='2',
            user=User.objects.create(
                id=3,
            )
        )

    def testMonth(self):
        Months.objects.get(date=timezone.now()) 
        Months.objects.get(hours='2')
        Months.objects.get(minutes='2')
        Months.objects.get(visits='2')
        Months.objects.get(publications='2')
        Months.objects.get(films='2')  
        Months.objects.get(user=3)


class EventsHistoryTest(TestCase):
    def setUp(self):
        EventsHistory.objects.create(
            date = timezone.now(),
            event='test-history-event',
            hours='2',
            minutes='2',
            visits='2',
            publications='2',
            films='2',
            studies='2',
            user=User.objects.create(
                id=4,
            ),
            month=Months.objects.create(
                id=1,
                date=timezone.now(),
            )
        )

    def testHistoryEvent(self):
        EventsHistory.objects.get(date=timezone.now()) 
        EventsHistory.objects.get(event='test-history-event')
        EventsHistory.objects.get(hours='2')
        EventsHistory.objects.get(minutes='2')
        EventsHistory.objects.get(visits='2')
        EventsHistory.objects.get(publications='2')
        EventsHistory.objects.get(films='2')
        EventsHistory.objects.get(studies='2')   
        EventsHistory.objects.get(user=4)
        EventsHistory.objects.get(month=1)


# class CalendarTest(TestCase):
#     def setUp(self):
