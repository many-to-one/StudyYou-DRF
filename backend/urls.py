from django.urls import path
from .views import *

urlpatterns = [
    path('events/<str:pk>/', getEvents, name='events'),
    path('events/<str:ev_pk>/<str:user_pk>/', getEvent, name='event'),
    path('events_history/<str:user_pk>/', getEventHistory, name='events_history'),
    path('event/create/<str:pk>/', createEvent, name='create-event'),
    path('events/<str:ev_pk>/<str:user_pk>/update/', updateEvent, name='update-event'),
    path('events/<str:ev_pk>/<str:user_pk>/delete/', deleteEvent, name='delete-event'),
    path('event/delete-all/<str:user_pk>/', deleteAll, name='delete-all'),
    path('results/<str:user_pk>/', getResults, name='results'),
    path('month/create/<str:user_pk>/<str:lng>/', getRecordedMonthResults, name='create_month_results'),
    path('get_months_results/<str:user_pk>/', getMonthsResults, name='get_month_results'),
    path('month/delete/<str:month_pk>/<str:user_pk>/', deleteMonthResult, name='delete_month_results'),
    path('images/', getImages, name='images'),
    path('images/<str:pk>', getImage, name='image'),
    path('set_calendar/<str:pk>/', setCalendar, name='set_calendar'),
    path('set_calendar_person/<str:pk>/', setCalendarPerson, name='set_calendar_person'),
    path('get_calendar/', getAllCalendarDates, name='get_calendars'),
    path('get_calendar_date/', getCalendarDatesByDate, name='get_calendar_date'),
    path('get_calendar_person/', getCalendarDatesByPerson, name='get_calendar_person'),
    path('delete_calendar/<str:pk>/', deleteCalendar, name='delete_calendar'),
    path('get_calendar_user/<str:pk>/', getCalendarDatesByUser, name='get_calendar_user'),
]