from multiprocessing import connection
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
from django.db import connection



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
    response_data = [{'message': 'Item added to cart'}]
    
    if request.method != 'POST':
        response_data = [{'error': 'Invalid request method'}]
        return JsonResponse(response_data, safe=False)
    
    request_data = json.loads(request.body)
    sessionid = request_data['generatedCode']
    productid = request_data['pid']
    productrate = request_data['rate']
    quantity = request_data['quantity']
    today_date = datetime.today().date()
    producttotal = int(productrate) * int(quantity)
    global stype
    stype=sessionid
    mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database='shopingcart')
    mycursor = mydb.cursor()

    # Check if the session already has a master order
    mycursor.execute("SELECT id FROM order_table_master WHERE sessionid = %s", (sessionid,))
    master_order = mycursor.fetchone()

    if master_order:
        omid = master_order[0]  # Get the existing master order ID
    else:
        # Create a new master order entry
        qmaster = "INSERT INTO order_table_master (sessionid, date) VALUES (%s, %s)"
        mycursor.execute(qmaster, (sessionid, today_date))
        mydb.commit()
        omid = mycursor.lastrowid  # Get the last inserted ID

    # Insert product details into ordertemp
    q = "INSERT INTO ordertemp (pid, omid, productprice, productqty, producttotal) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(q, (productid, omid, productrate, quantity, producttotal))
    mydb.commit()

    # Calculate and update the total in order_table_master
    mycursor.execute("SELECT SUM(producttotal) FROM ordertemp WHERE omid = %s", (omid,))
    total_product_totals = mycursor.fetchone()[0]

    update_total_query = "UPDATE order_table_master SET total = %s WHERE id = %s"
    mycursor.execute(update_total_query, (total_product_totals, omid))
    mydb.commit()

    mycursor.close()
    mydb.close()

    return JsonResponse(response_data, safe=False)

@csrf_exempt

def cartview(request):
    global stype
    phoneNumber = request.GET.get('phoneNumber')
    print('phonenumber cart test ',phoneNumber)
    print('sessionid', stype)
    mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database='shopingcart')
    mycursor = mydb.cursor()

    # Get the order_table_master ID for the given session
    q_order_master_id = "SELECT id FROM order_table_master WHERE sessionid = %s AND status='create' "
    mycursor.execute(q_order_master_id, (stype,))
    order_master_id = mycursor.fetchone()

    if order_master_id:
        # Get all the rows from ordertemp for the given order_table_master ID
        q_ordertemp = "SELECT * FROM ordertemp WHERE omid = %s AND status = 'create'"
        mycursor.execute(q_ordertemp, (order_master_id[0],))
        ordertemp_rows = mycursor.fetchall()

        formatted_data = []
        for ordertemp_row in ordertemp_rows:
            product_id = ordertemp_row[1]  # Product ID (pid) from ordertemp
            product_details_query = "SELECT * FROM products WHERE pid = %s"
            mycursor.execute(product_details_query, (product_id,))
            product_details = mycursor.fetchone()

            if product_details:
                data = {
                    'ordertemp_id': ordertemp_row[0],
                    'product_id': product_details[0],  # Product ID from products
                    'product_name': product_details[1],  # Product name from products
                    'product_price': product_details[2],  # Product price from products
                    'product_image':product_details[3],
                    'product_discretion':product_details[5],
                    

                    'product_quantity': ordertemp_row[5],  # Product quantity from ordertemp
                    'product_total': ordertemp_row[6],  # Product total from ordertemp
                    # Include other relevant details as needed
                }
                formatted_data.append(data)

        q_sum = "SELECT SUM(producttotal) FROM ordertemp WHERE omid = %s AND status = 'create'"
        mycursor.execute(q_sum, (order_master_id[0],))
        sum_result = mycursor.fetchone()
        total_price_sum = sum_result[0] if sum_result[0] is not None else 0
        
        q_total = "SELECT SUM(producttotal) AS total_sum FROM ordertemp WHERE omid = %s AND status = 'create'"
        mycursor.execute(q_total, (order_master_id[0],))
        total = mycursor.fetchone()
        print('total cart amount', total)

        mydb.close()

        response_data = {
            'cart_items': formatted_data,
            'total_price_sum': total_price_sum,
            'carttotal': total[0] if total else 0
        }

        return JsonResponse(response_data, safe=False)
    else:
        mydb.close()
        response_data = {'error': 'No cart items for the session'}
        return JsonResponse(response_data, safe=False)

    # This is the default return statement in case of unexpected errors
    return JsonResponse({'error': 'An unexpected error occurred'}, safe=False)



@csrf_exempt
def cartcomplete(request):
    request_data = json.loads(request.body)
    sessionid = request_data['generatedCode']
    pincode = request_data['pincode']
    country = request_data['country']
    state = request_data['state']
    city = request_data['city']
    name = request_data['userName']
    day = datetime.today().date()
    email = request_data['email']
    number = request_data['number']
    request.session['user_number'] = number
    request.session.save()

    # Establish MySQL connection
    mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database='shopingcart')
    mycursor = mydb.cursor()

    # Update query for order_table_master with parameterized placeholders
    update_order_master_query = "UPDATE order_table_master SET name = %s, city = %s, state = %s, country = %s, pincode = %s, phnumber = %s, email = %s WHERE sessionid = %s"
    update_order_master_values = (name, city, state, country, pincode, number, email, sessionid)

    # Execute the update query for order_table_master with parameterized values
    mycursor.execute(update_order_master_query, update_order_master_values)

    # Update query for ordertemp to update status
    update_ordertemp_query = "UPDATE ordertemp SET status = 'finish' WHERE omid IN (SELECT id FROM order_table_master WHERE sessionid = %s)"
    update_ordertemp_value = (sessionid,)

    # Execute the update query for ordertemp with parameterized values
    mycursor.execute(update_ordertemp_query, update_ordertemp_value)

    mydb.commit()

    mycursor.close()
    mydb.close()

    return JsonResponse(request_data, safe=False)



@csrf_exempt
def vieworderitem(request):
    try:
        phoneNumber = request.GET.get('phoneNumber')
        print(type(phoneNumber))
        global stype
        print('global print ', stype)
        data = [{'data': 'true'}]
        
        mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database='shopingcart')
        mycursor = mydb.cursor(buffered=True) 
        

        if phoneNumber is not None and phoneNumber != "null": 
            # Check if the provided phoneNumber is associated with an order
            q_order_master_id = "SELECT id FROM order_table_master WHERE phnumber = %s AND status = 'create'"
            mycursor.execute(q_order_master_id, (phoneNumber,))
            order_master_id = mycursor.fetchone()
            
        else:
            print('else work')
            # If phoneNumber is not provided, use the session (stype) for the query
            q_order_master_id = "SELECT id FROM order_table_master WHERE sessionid = %s AND status = 'create'"
            mycursor.execute(q_order_master_id, (stype,))
            order_master_id = mycursor.fetchone()
            
            

        if order_master_id:
            # Get all the rows from ordertemp for the given order_table_master ID
            q_ordertemp = "SELECT * FROM ordertemp WHERE omid = %s AND status = 'finish'"
            mycursor.execute(q_ordertemp, (order_master_id[0],))
            ordertemp_rows = mycursor.fetchall()

            formatted_data = []
            for ordertemp_row in ordertemp_rows:
                product_id = ordertemp_row[1]  # Product ID (pid) from ordertemp
                product_details_query = "SELECT * FROM products WHERE pid = %s"
                mycursor.execute(product_details_query, (product_id,))
                product_details = mycursor.fetchone()

                if product_details:
                    data = {
                        'ordertemp_id': ordertemp_row[0],
                        'product_id': product_details[0],  # Product ID from products
                        'product_name': product_details[1],  # Product name from products
                        'product_price': product_details[2],  # Product price from products
                        'product_image': product_details[3],
                        'product_discretion': product_details[5],
                        'product_quantity': ordertemp_row[5],  # Product quantity from ordertemp
                        'product_total': ordertemp_row[6],  # Product total from ordertemp
                        # Include other relevant details as needed
                    }
                    formatted_data.append(data)

            q_sum = "SELECT SUM(producttotal) FROM ordertemp WHERE omid = %s AND status = 'create'"
            mycursor.execute(q_sum, (order_master_id[0],))
            sum_result = mycursor.fetchone()
            total_price_sum = sum_result[0] if sum_result[0] is not None else 0

            q_total = "SELECT SUM(producttotal) AS total_sum FROM ordertemp WHERE omid = %s AND status = 'create'"
            mycursor.execute(q_total, (order_master_id[0],))
            total = mycursor.fetchone()
            print('total cart amount', total)
            mycursor.close()
            mydb.close()

            response_data = {
                'cart_items': formatted_data,
                'total_price_sum': total_price_sum,
                'carttotal': total[0] if total else 0
            }

            return JsonResponse(formatted_data, safe=False)
        else:
            mydb.close()
            response_data = {'error': 'No cart items found'}
            return JsonResponse(formatted_data, safe=False)
    except Exception as e:
        # Handle exceptions gracefully
        return JsonResponse({'error': str(e)}, status=500)

###################
# # view working
# def vieworderitem(request):
#     phoneNumber = request.GET.get('phoneNumber')
#     print('Phone Number:', phoneNumber) 
#     global stype
#     data=[{'data':'true'}]
#     mydb=mysql.connector.connect(host='localhost',user='root',password='root123',database='shopingcart')
#     mycursor=mydb.cursor()
#      # Get the order_table_master ID for the given session
#     q_order_master_id = "SELECT id FROM order_table_master WHERE sessionid = %s AND status='create' "
#     mycursor.execute(q_order_master_id, (stype,))
#     order_master_id = mycursor.fetchone()

#     if order_master_id:
#         # Get all the rows from ordertemp for the given order_table_master ID
#         q_ordertemp = "SELECT * FROM ordertemp WHERE omid = %s AND status = 'finish'"
#         mycursor.execute(q_ordertemp, (order_master_id[0],))
#         ordertemp_rows = mycursor.fetchall()

#         formatted_data = []
#         for ordertemp_row in ordertemp_rows:
#             product_id = ordertemp_row[1]  # Product ID (pid) from ordertemp
#             product_details_query = "SELECT * FROM products WHERE pid = %s"
#             mycursor.execute(product_details_query, (product_id,))
#             product_details = mycursor.fetchone()

#             if product_details:
#                 data = {
#                     'ordertemp_id': ordertemp_row[0],
#                     'product_id': product_details[0],  # Product ID from products
#                     'product_name': product_details[1],  # Product name from products
#                     'product_price': product_details[2],  # Product price from products
#                     'product_image':product_details[3],
#                     'product_discretion':product_details[5],
                    

#                     'product_quantity': ordertemp_row[5],  # Product quantity from ordertemp
#                     'product_total': ordertemp_row[6],  # Product total from ordertemp
#                     # Include other relevant details as needed
#                 }
#                 formatted_data.append(data)

#         q_sum = "SELECT SUM(producttotal) FROM ordertemp WHERE omid = %s AND status = 'create'"
#         mycursor.execute(q_sum, (order_master_id[0],))
#         sum_result = mycursor.fetchone()
#         total_price_sum = sum_result[0] if sum_result[0] is not None else 0
        
#         q_total = "SELECT SUM(producttotal) AS total_sum FROM ordertemp WHERE omid = %s AND status = 'create'"
#         mycursor.execute(q_total, (order_master_id[0],))
#         total = mycursor.fetchone()
#         print('total cart amount', total)
#         mycursor.close()
#         mydb.close()

#         response_data = {
#             'cart_items': formatted_data,
#             'total_price_sum': total_price_sum,
#             'carttotal': total[0] if total else 0
#         }

#         return JsonResponse(formatted_data, safe=False)
#     else:
#         mydb.close()
#         response_data = {'error': 'No cart items for the session'}
#         return JsonResponse(formatted_data, safe=False)

#     # This is the default return statement in case of unexpected errors
#     return JsonResponse({'error': 'An unexpected error occurred'}, safe=False)

#########
@csrf_exempt
def uservalidate(request):
    response_data = {'data': 'true'}
    request_data = json.loads(request.body)
    provided_number = request_data['number']
    
    mydb = mysql.connector.connect(host='localhost', user='root', password='root123', database='shopingcart')
    mycursor = mydb.cursor(buffered=True)  # Use buffered cursor
    
    try:
        # Check if the provided number is associated with an order
        q_order_master_id = "SELECT id FROM order_table_master WHERE phnumber = %s AND status = 'create'"
        mycursor.execute(q_order_master_id, (provided_number,))
        order_master_id = mycursor.fetchone()
        
        if order_master_id:
            omid = order_master_id[0]
            # Get all product details from ordertemp and products tables
            q_ordertemp = """
                SELECT o.pid, p.*
                FROM ordertemp o
                JOIN products p ON o.pid = p.pid
                WHERE o.omid = %s AND o.status = 'finish'
            """
            mycursor.execute(q_ordertemp, (omid,))
            ordertemp_rows = mycursor.fetchall()

            formatted_data = []
            for ordertemp_row in ordertemp_rows:
                data = {
                    'product_id': ordertemp_row[0],
                    'product_name': ordertemp_row[2],
                    'product_price': ordertemp_row[3],
                    'product_image': ordertemp_row[4],
                    # Include other product details here
                }
                formatted_data.append(data)

            response_data['cart_items'] = formatted_data

        else:
            response_data['error'] = 'No cart items for the provided number'

    except mysql.connector.Error as e:
        response_data['error'] = str(e)

    finally:
        mycursor.close()
        mydb.close()
    
    return JsonResponse(response_data, safe=False)

# setdemofinish