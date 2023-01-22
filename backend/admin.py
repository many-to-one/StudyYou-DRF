from django.contrib import admin

from .models import Event, HoursResult, Months


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

admin.site.register(Event, EventsAdmin)
admin.site.register(HoursResult, HoursResultAdmin)
admin.site.register(Months)
