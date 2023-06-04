import datetime
import io
import random

import jwt
from rest_framework.parsers import JSONParser
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from .models import createUsersModels, incident
from .serializers import usersSerializers, incidentSerializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def createUsers(request):
    if request.method == 'POST':
        body = request.body
        stream = io.BytesIO(body)
        pythonData = JSONParser().parse(stream)
        pythonData['password'] = make_password(pythonData['password'])
        serializers = usersSerializers(data=pythonData)
        if serializers.is_valid():
            try:
                serializers.save()
            except Exception as error:
                print(error)
                return JsonResponse({"message": "email used before"})
            return JsonResponse({'message': 'user created'})
        return JsonResponse({'Message': serializers.errors})

    return JsonResponse({'method not allowed'})


@csrf_exempt
def loginUserAndCreateJWTToken(request):
    if request.method == 'POST':
        body = request.body
        stream = io.BytesIO(body)
        pythonData = JSONParser().parse(stream)
        try:
            UserPasswordByEmail = createUsersModels.objects.get(email=pythonData['email'].strip())
        except Exception as error:
            print('loginUserAndCreateJWTToken', error)
            return JsonResponse({"Message:": "user does not exist"})
        serializeData = usersSerializers(UserPasswordByEmail)
        print(serializeData.data.get('email'))
        validUserOrNot = check_password(pythonData['password'], serializeData.data.get('password'))
        if validUserOrNot:
            print(validUserOrNot)
            # for JWT
            header = {
                "alg": "HS256",
                "typ": "JWT"
            }
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12),
                "id": serializeData.data.get('id'),
                "email": serializeData.data.get('email'),
                "userName": serializeData.data.get('first_name') + ' ' + serializeData.data.get('last_name')
            }
            secret = "secretkey"
            encoded_jwt = jwt.encode(payload, secret, algorithm='HS256', headers=header)
            print(encoded_jwt)
            return JsonResponse({"msg": "jwt created"})
        else:
            return JsonResponse({"message": 'enter password is wrong'})


def verifyJwtToken(token):
    jwtToken = token
    secret = "secretkey"
    try:
        tokenDetails = jwt.decode(jwtToken, secret, algorithms=['HS256'])
        return tokenDetails, True
    except Exception as error:
        print(error)
        return JsonResponse({'message': 'token expired login and create new token'})


def generateIncidentID():
    randomID = 'RMG' + str(random.randrange(10000, 99999, 5)) + str(datetime.date.today().year)
    return randomID


def checkForUniqueIncidentID(incidentID):
    data = None
    try:
        data = incident.objects.get(incident_id=incidentID)
    except Exception as error:
        print(error, 'no incident ID exist')

    while data:
        incidentID = generateIncidentID()
        data = incident.objects.get(incident_id=incidentID)
    return incidentID


def viewIncidents(request):
    if request.method == 'GET':
        token = request.headers['token']
        userDetails, JwtVerify = verifyJwtToken(token)
        userID = userDetails['id']
        try:
            data1 = incident.objects.filter(user_id=userID)
            print(data1)
        except Exception as error:
            print(error)
            return JsonResponse({"msg": ' no records found for this user :' + str(userDetails['userName'])})
        incdntSerializers = incidentSerializers(data1, many=True)
        print(incdntSerializers)
        return JsonResponse(incdntSerializers.data, safe=False)


@csrf_exempt
def incidentDetails(request):
    token = request.headers['token']
    userDetails, JwtVerify = verifyJwtToken(token)
    if request.method == 'POST':
        body = request.body
        stream = io.BytesIO(body)
        pythonData = JSONParser().parse(stream)
        print(pythonData)
        incidentID = generateIncidentID()
        incidentID = checkForUniqueIncidentID(incidentID)
        pythonData['incident_id'] = incidentID
        pythonData['user_id'] = userDetails['id']
        pythonData['reported_date'] = datetime.datetime.now()
        pythonData['reporter_name'] = userDetails['userName']
        serializersData = incidentSerializers(data=pythonData, partial=True)
        if serializersData.is_valid():
            try:
                serializersData.save()
            except Exception as error:
                print(error)
                return JsonResponse({"msg": "error occurred during inserting data into db"})
            return JsonResponse({'msg': 'user incident successfully inserted'})
        return JsonResponse({'msg': serializersData.errors})
    elif request.method == 'PUT':
        body = request.body
        stream = io.BytesIO(body)
        pythonData = JSONParser().parse(stream)
        instanceID = pythonData['id']
        instanceDetails = incident.objects.get(id=instanceID, user_id=userDetails['id'])
        # checking for closed incidents
        if instanceDetails.Incident_status == 'closed':
            return JsonResponse({"msg": "incident closed not updated "})
        serializersData = incidentSerializers(instanceDetails, data=pythonData, partial=True)
        if serializersData.is_valid():
            try:
                serializersData.save()
            except Exception as error:
                print(error)
                return JsonResponse({'msg': "error occurred during updating incidents"})
            return JsonResponse({'msg': 'Incident updated'})
        return JsonResponse({'msg': serializersData.errors})
    return JsonResponse({'msg': 'method not allowed'})


def searchIncidentsByIncidentID(request):
    token = request.headers['token']
    userDetails, JwtVerify = verifyJwtToken(token)
    if request.method == 'GET':
        body = request.body
        stream = io.BytesIO(body)
        pythonData = JSONParser().parse(stream)
        incidentID = pythonData['incidentID']
        data = incident.objects.filter(incident_id=incidentID, user_id=userDetails['id'])
        if not data:
            return JsonResponse({"msg": 'No records Found regarding this ID:'+str(incidentID)})
        serializedData = incidentSerializers(data, many=True)
        return JsonResponse(serializedData.data, safe=False)
    return JsonResponse({"msg": "Method not allowed"})


