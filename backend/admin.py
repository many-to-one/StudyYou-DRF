from django.contrib import admin

from .models import Event


class EventsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'event',
    )

admin.site.register(Event, EventsAdmin)
