import time
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
import mysql.connector
import json
from datetime import datetime, timedelta


# Create your views here.
stype=''
def home(request):
    mydb=mysql.connector.connect(host='localhost',user='root',password='root123',database='shopingcart')
    mycursor=mydb.cursor()
    q="select *from products"
    print(q)
    mycursor.execute(q)
    row=mycursor.fetchall()
    formatted_data = []

    for rows in row:
        data = dict(zip(mycursor.column_names, rows))
        formatted_data.append(data)

    mydb.close()
    print(type(row))
       
    return JsonResponse( formatted_data ,safe=False)
@csrf_exempt
def cartitemadd(request):
     response_data=[{'hi':'add cart'}]
     request_data = json.loads(request.body)
     sessionid=request_data['generatedCode']
     productid=request_data['pid']
     productname=request_data['name']
     productrate=request_data['rate']
     shorttag=request_data['shortdiscretion']
     productimage=request_data['imageurl']
     fulltag=request_data['discretion']  
     quantity=request_data['quantity']
     today_date = datetime.today().date()
     producttotal=int(productrate)*int(quantity)
     global stype
     stype=sessionid
     mydb=mysql.connector.connect(host='localhost',user='root',password='root123',database='shopingcart')
     mycursor=mydb.cursor()
     q="insert into ordertemp (pid,sessionid,date,pname,productprice,productimage,productfulldescription,productshortdescription,productqty,producttotal)values ('"+str(productid)+"','"+str(sessionid)+"','"+str(today_date)+"','"+str(productname)+"','"+str(productrate)+"','"+str(productimage)+"','"+str(fulltag)+"','"+str(shorttag)+"','"+str(quantity)+"','"+str(producttotal)+"')"
     mycursor.execute(q)
     mydb.commit()
     mydb.close()
     return JsonResponse( response_data,safe=False)

@csrf_exempt
def cartview(request):
    global stype
    print('sessionid',stype)
    data=[{'cartview':'cartview'}]
    mydb=mysql.connector.connect(host='localhost',user='root',password='root123',database='shopingcart')
    mycursor=mydb.cursor()
    # q="select *from ordertemp where sessionid='"+str(stype)+"'"
    q="select *from ordertemp where sessionid='"+str(stype)+"'AND status='create'"
    print(q)
    mycursor.execute(q)
    row=mycursor.fetchall()
    formatted_data = []

    for rows in row:
        data = dict(zip(mycursor.column_names, rows))
        formatted_data.append(data)

    q_sum = "SELECT SUM(producttotal) FROM ordertemp WHERE sessionid='"+str(stype)+"'AND status='create'"
    mycursor.execute(q_sum)
    sum_result = mycursor.fetchone()
    total_price_sum = sum_result[0] if sum_result[0] is not None else 0      
    q_total="SELECT SUM(producttotal) AS total_sum FROM ordertemp where sessionid='"+str(stype)+"'AND status='create'"
    mycursor.execute(q_total)
    total=mycursor.fetchone()
    print('total cart amount',total)
    mydb.close()
    response_data = {
        'cart_items': formatted_data,
        'total_price_sum': total_price_sum, # Include total_price_sum in the response
        'carttotal':total
    }
    print(type(row))
    
    return JsonResponse( response_data,safe=False)


@csrf_exempt
def cartcomplete(request):
    request_data = json.loads(request.body)
    sessionid=request_data['generatedCode']
    pincode=request_data['pincode']
    country=request_data['country']
    state=request_data['state']
    city=request_data['city']
    name=request_data['userName']
    day=datetime.today().date()
    mydb=mysql.connector.connect(host='localhost',user='root',password='root123',database='shopingcart')
    mycursor=mydb.cursor()
    # test take total amount
    q_sum = "SELECT SUM(producttotal) FROM ordertemp WHERE sessionid = '" + str(sessionid) + "'"
    mycursor.execute(q_sum)
    sum_result = mycursor.fetchone()
    total_price_sum = sum_result[0] if sum_result[0] is not None else 0      
    q_total="SELECT SUM(producttotal) AS total_sum FROM ordertemp where sessionid='"+str(sessionid)+"'" 
    mycursor.execute(q_total)
    total=mycursor.fetchone()
    total_str=str(total_price_sum)
    print('total cart amount',total_str,type(total_str))
    # test end
    q="insert into order_table_master (sessionid,date,total,name,city,state,country,pincode)values('"+str(sessionid)+"','"+str(day)+"','"+str(total_str)+"','"+str(name)+"','"+str(city)+"','"+str(state)+"','"+str(country)+"','"+str(pincode)+"')"
    mycursor.execute(q)
    mydb.commit()
    statusset="UPDATE order_table_master AS otm JOIN ordertemp AS ot ON otm.sessionid = ot.sessionid SET otm.status = 'finish', ot.status = 'finish' WHERE otm.sessionid = '"+str(sessionid)+"'"
    mycursor.execute(statusset)
    mydb.commit()
    mydb.close()
    return JsonResponse( request_data,safe=False)

