from django.shortcuts import render
import joblib
import os
import yaml
import pandas as pd
from .models import flight_fare

# Create your views here.

def index(request):
    return render(request, 'index.html')

def result(request):
    model = joblib.load('../prediction_service/model/model.joblib')
    list_ = []
    list_.append(int(request.GET['Airline']))
    list_.append(int(request.GET['Source']))
    list_.append(int(request.GET['Destination']))
    list_.append(int(request.GET['Total_Stops']))
    list_.append(int(request.GET['Journey_Day']))
    list_.append(int(request.GET['Journey_month']))
    list_.append(int(request.GET['Dep_Hour']))
    list_.append(int(request.GET['Dep_Min']))
    list_.append(int(request.GET['Arrival_Hour']))
    list_.append(int(request.GET['Arrival_min']))
    list_.append(int(request.GET['Duration_hours']))
    list_.append(int(request.GET['Duration_mins']))

    answer = model.predict([list_]).tolist()[0]

    b = flight_fare(
        Airline=request.GET['Airline'],
        Source=request.GET['Source'],
        Destination=request.GET['Destination'],
        Total_Stops=request.GET['Total_Stops'],
        Journey_Day=request.GET['Journey_Day'],
        Journey_month=request.GET['Journey_month'],
        Dep_Hour=request.GET['Dep_Hour'],
        Dep_Min=request.GET['Dep_Min'],
        Arrival_Hour=request.GET['Arrival_Hour'],
        Arrival_min=request.GET['Arrival_min'],
        Duration_hours=request.GET['Duration_hours'],
        Duration_mins=request.GET['Duration_mins'],
        Price=answer,
    )
    b.save()

    return render(request, 'index.html', {'answer': answer})
