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
        users = User.objects.filter(
            congregation=data['congregation'],
            stand=True,
        ).exclude(
            groupe=1,
        )
        udl = []
        for a in users:
            udl.append(a.username)
        ud = sample(udl, len(udl))

    dates = data['date']
    date = []
    di = ''
    count = 0

    for d in dates:
        count += 1
        di += d
        if d == ',' or count == 43:
            date.append(di[:10])
            di = ''

    place = ['Park przy zamku', 'Skrzyżowanie Centrum', 'Wjazd do Galerii']

    time_Tue = [f'{date[0]} 10:00 - 11:00', f'{date[0]} 11:00 - 12:00', f'{date[0]} 12:00 - 13:00', f'{date[0]} 13:00 - 14:00']
    time_Thu = [f'{date[1]} 10:00 - 11:00', f'{date[1]} 11:00 - 12:00', f'{date[1]} 16:00 - 17:00', f'{date[1]} 17:00 - 18:00']
    time_Fri = [f'{date[2]} 10:00 - 11:00', f'{date[2]} 11:00 - 12:00', f'{date[2]} 16:00 - 17:00', f'{date[2]} 17:00 - 18:00']
    time_Sat = [f'{date[3]} 09:00 - 10:00', f'{date[3]} 10:00 - 11:00', f'{date[3]} 11:00 - 12:00', f'{date[3]} 12:00 - 13:00']

    ##############################################################
    ####################### Tuesday ##############################
    ##############################################################

    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[0],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[0],
                    user = User.objects.get(username=ud[0]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[1],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[0],
                    user = User.objects.get(username=ud[1]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[2],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[1],
                    user = User.objects.get(username=ud[2]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[3],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[1],
                    user = User.objects.get(username=ud[3]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[4],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[2],
                    user = User.objects.get(username=ud[4]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[5],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[2],
                    user = User.objects.get(username=ud[5]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[6],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[3],
                    user = User.objects.get(username=ud[6]),
                    )
    calendar = Calendar.objects.create(
                    date = date[0],
                    action = data['action'],
                    person = ud[7],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Tue[3],
                    user = User.objects.get(username=ud[7]),
                    )
    
    ##############################################################
    ####################### Thursday #############################
    ##############################################################
    
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[8],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[0],
                    user = User.objects.get(username=ud[8]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[9],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[0],
                    user = User.objects.get(username=ud[9]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[10],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[1],
                    user = User.objects.get(username=ud[10]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[11],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[1],
                    user = User.objects.get(username=ud[11]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[12],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[2],
                    user = User.objects.get(username=ud[12]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[13],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[2],
                    user = User.objects.get(username=ud[13]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[14],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[3],
                    user = User.objects.get(username=ud[14]),
                    )
    calendar = Calendar.objects.create(
                    date = date[1],
                    action = data['action'],
                    person = ud[15],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Thu[3],
                    user = User.objects.get(username=ud[15]),
                    )
    
    ##############################################################
    ######################## Friday ##############################
    ##############################################################

    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[16],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[0],
                    user = User.objects.get(username=ud[16]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[17],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[0],
                    user = User.objects.get(username=ud[17]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[18],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[1],
                    user = User.objects.get(username=ud[18]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[19],
                    place = place[0],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[1],
                    user = User.objects.get(username=ud[19]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[20],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[2],
                    user = User.objects.get(username=ud[20]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[21],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[2],
                    user = User.objects.get(username=ud[21]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[22],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[3],
                    user = User.objects.get(username=ud[22]),
                    )
    calendar = Calendar.objects.create(
                    date = date[2],
                    action = data['action'],
                    person = ud[23],
                    place = place[2],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Fri[3],
                    user = User.objects.get(username=ud[23]),
                    )
    
    ##############################################################
    ######################## Satday ##############################
    ##############################################################

    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[24],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[0],
                    user = User.objects.get(username=ud[24]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[25],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[0],
                    user = User.objects.get(username=ud[25]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[5],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[1],
                    user = User.objects.get(username=ud[5]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[0],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[1],
                    user = User.objects.get(username=ud[0]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[1],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[2],
                    user = User.objects.get(username=ud[1]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[2],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[2],
                    user = User.objects.get(username=ud[2]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[3],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[3],
                    user = User.objects.get(username=ud[3]),
                    )
    calendar = Calendar.objects.create(
                    date = date[3],
                    action = data['action'],
                    person = ud[4],
                    place = place[1],
                    icon = data['icon'],
                    congregation = data['congregation'],
                    time = time_Sat[3],
                    user = User.objects.get(username=ud[4]),
                    )

    serializer = CalendarSerializer(calendar, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )

# from fpdf import FPDF
# import os
@api_view(['GET']) 
def getRandomStandBig(request, congregation): 
    stands = Calendar.objects.filter(
        congregation=congregation,
        action='Stand',
    )
    serializer = CalendarSerializer(stands, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
        )

    # filename = 'Owoc.txt'
    # dir_path = r'D:\IT\ework\Owoc'
    # path = os.path.join(dir_path, filename) 
    # with open(path, 'w') as f:
    #     for stand in stands:
    #         f.write(stand.person)
    #         f.write(' === ')
    #         f.write(stand.time)
    #         f.write('\n')

    # import csv
    # data = []
    # filename = 'Owoc.csv'
    # dir_path = r'D:\IT\ework\Owoc'
    # path = os.path.join(dir_path, filename) 
    # for stand in stands:
    #     data.append([stand.person, stand.time])
    # with open(path, 'w', encoding='UTF8', newline='')as f:
    #     writer = csv.writer(f)
    #     writer.writerows(data)

    # df = pd.DataFrame(
    #       {'GŁOSICIELE' : persons,
    #        'GODZINY' : times,
    #       })
    # pdf = FPDF()
    # pdf.add_page()
    # ch = 50
    # # Table Header
    # pdf.set_font('Arial', 'B', 16)
    # pdf.cell(w=40, h=ch, txt='GŁOSICIELE', border=1, ln=0, align='C')
    # pdf.cell(w=40, h=ch, txt='GODZINY', border=1, ln=1, align='C')
    # # Table contents
    # pdf.set_font('Arial', '', 16)
    # for i in range(0, len(df)):
    #     pdf.cell(w=40, h=ch, 
    #              txt=df['GŁOSICIELE'].iloc[i].encode('latin-1'), 
    #              border=1, ln=0, align='C')
    #     pdf.cell(w=40, h=ch, 
    #              txt=df['GODZINY'].iloc[i], 
    #              border=1, ln=1, align='C')
    # directory = 'Owoc'
    # parent_dir = 'D:\IT\ework'
    # path = os.path.join(parent_dir, directory) 
    # os.makedirs(path)
    # pdf.output(f'parent_dir/example.pdf', 'F')