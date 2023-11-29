from collections import namedtuple
import mysql.connector

from restoServices import placeOrder

from dishes import Dishes

if __name__=='__main__':
 mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sk@19302519@sql',
    database='resto'
  )
 cursor = mydb.cursor(dictionary=True,buffered=True)
 cursor.execute("SELECT * FROM dishes")

 data = cursor.fetchall()

 dishes=[namedtuple("Dishes", i.keys())(*i.values()) for i in data]

print("Welcome to Resto The Restaurant")
name=input("Enter you name: ")
email=input("Enter your email id: ")
print("Enter the id of the dish and quantity to add food to order")
print("Enter 1 to continue  order and 0 to confirm order")

userIp=1
cart={}
while(userIp==1):
   for i in dishes:
      print(i.id,i.name,i.type,i.cost,sep=" ",end="\n")
   dishId=int(input("Enter the dish id: "))
   qty=int(input("Enter the qty: "))
   cart[dishId]=qty
   userIp=int(input("You wanna continue? press 1 or press 0 to confirm order"))
final=placeOrder(name,email,cart)
print("your final price is: ",round(final))






















