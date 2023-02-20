from django.contrib import admin

from .models import Calendar, Event, HoursResult, Months, EventsHistory


class EventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'event',
    )


class HoursResultAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'hours', 
        'minutes',
        'visits',
        'publications',
        'films',
        )  


class CalendarAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'user',
    ) 
        

admin.site.register(Event, EventsAdmin)
admin.site.register(HoursResult, HoursResultAdmin)
admin.site.register(Months)
admin.site.register(EventsHistory)
admin.site.register(Calendar, CalendarAdmin)
