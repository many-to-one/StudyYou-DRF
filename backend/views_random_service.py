from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users_app.models import User
from users_app.utils import Util
from .serializers import CalendarSerializer
from .models import Calendar
from random import sample
import pandas as pd


@api_view(['POST', 'GET', 'DELETE']) 
def setRandomStandBig(request):   
    if request.method == 'POST':
        data = request.data
