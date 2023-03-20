from rest_framework import serializers
from .models import Calendar, Event, Image, Months, EventsHistory, HoursResult, PlacesStand


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HoursResult
        fields = "__all__"
        # fields = [
        #     'date',
        #     'hours', 
        #     'minutes',
        #     'publications',
        #     'visits',
        #     'films',
        # ]


class MonthsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Months
        fields = "__all__"


class EventsHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventsHistory  
        fields = "__all__"      


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = "__all__"


class CalendarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Calendar
        fields = "__all__"


class PlacesStandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PlacesStand
        fields = "__all__"