from django.contrib import admin

from .models import Calendar, Event, HoursResult, Months, EventsHistory, PlacesStand


class EventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        # 'event',
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
        'action',
        'person',
        'user',
    ) 


class PlacesStandAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


class MonthsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'date',
    )
        

admin.site.register(Event, EventsAdmin)
admin.site.register(HoursResult, HoursResultAdmin)
admin.site.register(Months, MonthsAdmin)
admin.site.register(EventsHistory)
admin.site.register(Calendar, CalendarAdmin)
admin.site.register(PlacesStand, PlacesStandAdmin)
