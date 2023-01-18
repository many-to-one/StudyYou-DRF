from rest_framework import serializers
from .models import Event, Image, Months


class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = "__all__"


class MonthsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Months
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = "__all__"