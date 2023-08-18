import time
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import mysql.connector
import json
import uuid
from datetime import datetime, timedelta
# Create your views here.

def home(request):
     response_data=[{'hi':'data'},{'test':'file'}]
     return JsonResponse( response_data,safe=False)
def product(request):
     response_data=[{'hi':'product data'},{'test':'product file'}]
     return JsonResponse( response_data,safe=False)