from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import NationalId, Visit
from .serializer import NationalIdSerializer, VisitSerializer
from django.http import HttpResponse, JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
import logging,traceback
logger = logging.getLogger('django')


#Limiting the rate to only 10 per minute for testing purposes
@ratelimit(key='user_or_ip', rate='10/m')
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def validate_id(request):
    
    ###Get username and update visits count in database
    logger.info(request.user)
    try:
        visit = Visit.objects.get(username=request.user)
        visit.count +=1
        visit.save()
        logger.info('User visit counts incremented')
    except Visit.DoesNotExist:
        visit = Visit()
        visit.username = request.user
        visit.count = 1
        visit.save()
        logger.info('New record for user created')

    logger.info("Validating id number")
    serializer = NationalIdSerializer(data=request.data)
    if serializer.is_valid():
        number = serializer.validated_data['number']
        logger.info('ID number: '+number)
        #Get generation, year, month and day
        gen = number[0:1]
        if(gen =='2'):
            birthStart = '19'
        elif(gen =='3'):
            birthStart = '20'
        else: 
            return Response({'message':'First number has to be 2 or 3','code':500})
 

        year = number[1:3]
        month = number[3:5]
        day = number[5:7]

        birthDate = day +'/'+month +'/'+ birthStart+year 

        #Validate Birthdate
        try:
            dateObject = datetime.strptime(birthDate,'%d/%m/%Y')
        except ValueError:
            return Response({'message':'Invalid birthdate','code':500})
        
        #Get Country Code
        cityCode = number[7:9]



        return Response({'birthDate':birthDate,
                         'city':cityCode}, status=status.HTTP_200_OK)
    else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_visits(request):
    visits = Visit.objects.all()
    serializer = VisitSerializer(visits, many=True)
    return Response(serializer.data)




