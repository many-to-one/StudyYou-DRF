from django.urls import path
from .views import *
from .views_random_stand import *
from .views_random_service import *
from .views_random_ministry import *
from .views_random_week import *

urlpatterns = [
    path('events/<str:pk>/', getEvents, name='events'),
    path('events/<str:ev_pk>/<str:user_pk>/', getEvent, name='event'),
    path('events_history/<str:user_pk>/', getEventHistory, name='events_history'),
    path('event/create/<str:pk>/', createEvent, name='create-event'),
    path('events/<str:ev_pk>/<str:user_pk>/update/', updateEvent, name='update-event'),
    path('events/<str:ev_pk>/<str:user_pk>/delete/', deleteEvent, name='delete-event'),
    path('event/delete-all/<str:user_pk>/', deleteAll, name='delete-all'),
    path('results/<str:user_pk>/', getResults, name='results'),
    path('month/create/<str:user_pk>/<str:lng>/<str:studies>/<str:month>/', getRecordedMonthResults, name='create_month_results'),
    path('get_months_results/<str:user_pk>/', getMonthsResults, name='get_month_results'),
    path('month/delete/<str:month_pk>/<str:user_pk>/', deleteMonthResult, name='delete_month_results'),
    path('delete_all_months_results/<str:user_pk>/', deleteAllMonthsResults, name='delete_all_months_results'),
    path('images/', getImages, name='images'),
    path('images/<str:pk>', getImage, name='image'),
    path('set_calendar/<str:pk>/<str:week_ago>/', setCalendar, name='set_calendar'),
    path('set_calendar_person/<str:pk>/', setCalendarPerson, name='set_calendar_person'),
    path('set_calendar_from_person/<str:username>/', setCalendarFromPerson, name='set_calendar_from_person'),
    path('set_calendar_stand/<str:username>/', setCalendarStand, name='set_calendar_stand'),
    path('update_calendar_stand/<str:pk>/', updateCalendarStand, name='update_calendar_stand'),
    path('get_calendar/', getAllCalendarDates, name='get_calendars'),
    path('get_calendar_date/', getCalendarDatesByDate, name='get_calendar_date'),
    path('get_calendar_person/', getCalendarDatesByPerson, name='get_calendar_person'),
    path('delete_calendar/<str:pk>/', deleteCalendar, name='delete_calendar'),
    path('get_calendar_user/<str:pk>/', getCalendarDatesByUser, name='get_calendar_user'),
    path('set_calendar_speach/', setCalendarSpeach, name='set_calendar_speach'),
    path('set_calendar_speach_from_list/<str:pk>/', setCalendarSpeachFromList, name='set_calendar_speach_from_list'),
    path('set_places_stand/<str:congregation>/', setPlacesStand, name='set_places_stand'),
    path('set_random_stand_big/', setRandomStandBig, name='set_random_stand_big'),
    path('get_random_stand_big/<str:congregation>/', getRandomStandBig, name='get_random_stand_big'),
    path('set_random_service/', setRandomService, name='set_random_service'),
    path('set_random_ministry/', setRandomMinistry, name='set_random_ministry'),
    path('set_random_weeks/', setRandomWeek, name='set_random_week'),
]