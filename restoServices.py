import mysql.connector
from collections import namedtuple
from fpdf import FPDF
import os
from datetime import date
from filestack import Client
import mailtrap as mt
from orders import Orders



orddb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sk@19302519@sql',
    database='resto'
)

pdf=FPDF(orientation='P',unit='pt',format='A4')
cursor = orddb.cursor(dictionary=True, buffered=True)
cursor.execute("SELECT * from dishes")
data=cursor.fetchall()
dishes=[namedtuple("Dishes",dish.keys())(*dish.values()) for dish in data]
dishesDict={d.id:[d.cost,d.name] for d in dishes}




def placeOrder(name,email,cart):
    #print(dishesDict)
    ordCursor = orddb.cursor(buffered=True)
    ordCursor.execute("SELECT * FROM orders")
    id=ordCursor.rowcount+100
    insertStmt="INSERT into orders(id,name,email,dish_id,qty,total) VALUES(%s,%s,%s,%s,%s,%s)"

    for k in cart.keys():
        dish_id=k
        qty=cart[k]
        total=calcCost(dish_id,qty)
        ordCursor.execute(insertStmt,(id,name,email,dish_id,qty,total))
        orddb.commit()

    return generateBill(name,email,id)


def calcCost(id,qty):
    result=0
    result=qty*dishesDict[id][0]+50
    return result

def generateBill(name,email,id):
    finalTotal=0
    cursor=orddb.cursor(buffered=True,dictionary=True)
    cursor.execute("SELECT * FROM orders")
    orders=cursor.fetchall()
    orderList=[namedtuple("Orders",o.keys())(*o.values()) for o in orders]
    #print(orderList)
    pdf.add_page()
    setFont(style='B')
    pdf.cell(w=0,h=100,txt='Resto The Restaurant',border=0,align='C',ln=1)
    setFont(size=24,style="B")
    pdf.cell(w=0,h=100,txt=name+"\n"+email,align='L')
    pdf.cell(w=0,h=100,txt=str(date.today()),align='R',ln=1)
    pdf.cell(w=0,h=0,txt=str(id),align='L',ln=1)
    pdf.cell(w=200,h=100,txt="Dish")
    pdf.cell(w=100, h=100, txt="Cost")
    pdf.cell(w=100,h=100,txt="Quantity")
    pdf.cell(w=100,h=100,txt="Total",align='R',ln=1)
    setFont(size=20)
    for ord in orderList:
       if id==ord.id:
           pdf.cell(w=200, h=30, txt=dishesDict[ord.dish_id][1])
           pdf.cell(w=100, h=30, txt=str(dishesDict[ord.dish_id][0]))
           pdf.cell(w=100, h=30, txt=str(ord.qty),align='R')
           pdf.cell(w=100, h=30, txt=str(ord.total),align='R', ln=1)
           finalTotal+=ord.total
    setFont(size=22,style='B')
    pdf.cell(w=0,h=100,txt='Total',align='L')
    pdf.cell(w=0,h=100,txt=str(round(finalTotal)),align='R',ln=1)
    pdf.cell(w=550,h=200,txt='Thank You for Choosing us!!',align='C')
    os.chdir("bills")
    pdf.output(email+"-"+str(id)+".pdf")
    fileUpload(email+"-"+str(id)+".pdf",email)
    return finalTotal

def fileUpload(path,email):
    client=Client("AFDAvzkcjT7C2WKFAa0edz")
    pdfLink=client.upload(filepath=path)
    url=pdfLink.url

    print(url)



def setFont(size=26,style='',family='Times'):
    pdf.set_font(family=family,size=size,style=style)



