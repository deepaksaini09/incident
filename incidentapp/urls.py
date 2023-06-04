from django.urls import path
from . import views
urlpatterns = [
    path('createUsers', views.createUsers, name='loginUserAndCreateJWTToken'),
    path('loginUserAndCreateJWTToken', views.loginUserAndCreateJWTToken, name='loginUserAndCreateJWTToken'),
    path('viewIncidents', views.viewIncidents, name='viewIncidents'),
    path('incidentDetails', views.incidentDetails, name='incidentDetails'),
    path('searchIncidentsByIncidentID', views.searchIncidentsByIncidentID, name='searchIncidentsByIncidentID')
]
