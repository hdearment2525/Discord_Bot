# Hunter DeArment Conner Botte


import discord
import os
import smtplib
from replit import db
import random
from os import system
import mysql.connector

mydb = mysql.connector.connect(
  host = "216.137.177.30",
  user = "team3",
  password = "UpdateTrello!1",
  database = "testDB"
)

print(mydb)


client = discord.Client()


class user_order():
  def __init__(self,email,id1,price):
    self.email = email
    self.id1 = id1
    self.price = price

users = {}


db['email'] = []

# item Dictionary
items = {'a':"Apple",'b':"Bread",'c':"Car",'d':"Dog Toy",'e':"Electric Scooter",'f':"Fan",'g':"Grapes",'h':"Horn",'i':"Irish Coffee",'j':"Jump Rope",'k':"Kite",'l':"Long Socks",'m':"Mushroom",'n':"Notebook",'o':"Oranges",'p':"Piano",'q':"Quilt",'r':"Rain Coat",'s':"Suv",'t':"Trench Coat",'u':"Umbrella",'v':"Violin",'w':"Windshield",'x':"Xylophone",'y':"YoYo",'z':"Zebra Striped Pants",'0':"Banana",'1':"Lemon",'2':"Car Air Freshner",'3':"Car Seat",'4':"Denim Jacket",'5':"Daisy Dukes",'6':"Chello",'7':"Trumpet",'8':"Surf Board",'9':"Rubix Cube"}

prices = {'a':3.25,'b':4.50,'c':1029.00,'d':10.57,'e':39.99,'f':24.99,'g':3.99,'h':23.50,'i':5.99,'j':9.99,'k':15.99,'l':3.49,'m':7.99,'n':8.99,'o':5.65,'p':300.29,'q':9.99,'r':79.99,'9':5.00, '8':30.00,'7':50.00,'6':200.00,'5':30.00,'4':40.00,'3':200.00,'2':1.00,'1':1.00,'0':1.00,'z':20.00,'y':3.00,'x':10.00,'w':500.00,'v':60.00,'u':10.00,'t':50.00,'s':40000.00}

# Split into categories for recommendations
food = [items['a'],items['b'],items['g'],items['i'],items['m'],items['o'],items['0'],items['1']]

car_stuff = [items['c'],items['h'],items['s'],items['w'],items['2'],items['3']]

clothes = [items['l'],items['r'],items['t'],items['z'],items['4'],items['5']]

toys = [items['j'],items['k'],items['p'],items['v'],items['x'],items['y'],items['6'],items['7'],items['9']]

misc = [items['d'],items['e'],items['f'],items['n'],items['q'],items['9']]

# checks if email is a valid email
def valid_email(em):
  letters = 'abcdefghijklmnopqrstuvwxyz'
  if type(em) == str:
    em.lower()
    if em[0] in letters:
      if '@' in em and '.com' in em:
        if em.index('@') < em.index('.com'):
          return True
        else:
          return False
      else:
        return False
    else:
      return False
  else:
    return False



# adds email to list withing db
def add_user(email):
  if email not in db['email']:
    print(db['email'])
    db['email'].append(email)
    print(db['email'])

# finds the index of specific email in database
def find_index(email):
  count = 0
  for i in db['email']:
    if i == email:
      return count
    count += 1

# adds class order to list of users
def add_order(email,id):
  a = str(id)
  a = a[0]
  current = user_order(email,id,prices[a])
  users[current.email] = current

# Recs an item based on past orders
def rec(email):

  rec = users[str(email)].id1

  index = rec[0]
  print(index)
  item = ""

  while True:

    if items[index] in car_stuff:
      num = random.randint(0,len(car_stuff)-1)
      no_num = car_stuff.index(items[index])
      if num == no_num:
        continue
      else:
        item = car_stuff[num]
        print(item)
        return item
    elif items[index] in food:
      num = random.randint(0,len(food)-1)
      no_num = food.index(items[index])
      if num == no_num:
        continue
      else:
        item = food[num]
        print(item)
        return item

    elif items[index] in clothes:
      num = random.randint(0,len(clothes)-1)
      no_num = clothes.index(items[index])
      if num == no_num:
        continue
      else:
        item = clothes[num]
        print(item)
        return item
    elif items[index] in toys:
      num = random.randint(0,len(toys)-1)
      no_num = toys.index(items[index])
      if num == no_num:
        continue
      else:
        item = toys[num]
        print(item)
        return item
    elif items[index] in misc:
      num = random.randint(0,len(misc)-1)
      no_num = misc.index(items[index])
      if num == no_num:
        continue
      else:
        item = misc[num]
        print(item)
        return item
    else:
      item = "Nothing"
      return item
  
# returns all items under given price
def under(price):
  lst = []
  for i in prices:
    if prices[i] < price:
      lst.append(items[i])
  
  return lst


def cancel_order(email,order_number):
    confirmedEmail = False
    confirmedOrder = False
    
    for i in db['email']:
      if i == email:
        confirmedEmail = True
      else:
        continue
      
    for i in users:
      if order_number == users[i].id1:
        confirmedOrder = True
      else:

        continue

    if confirmedEmail and confirmedOrder:
      return True
    else:
      return False    

      
def send_confirmation(user, password, recipient, subject, body):
    gmail_user = user
    gmail_pwd = password
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('-add_email'):
      user = message.content.split()
      if valid_email(user[1]):
        add_user(user[1])
        await message.channel.send(user[1] + " added!")
      else:
        await message.channel.send(user[1] + " is an invalid email!")

    if message.content.startswith('-confirm_order'):
      user_input = message.content.split()
      tempEmail = user_input[1]
      tempOrder = user_input[2]
      if (cancel_order(tempEmail,tempOrder)):
        send_confirmation("testemail19872614@gmail.com" , "Abc123614!" , tempEmail , "Confirmation" , "Hello, " + tempEmail + " " + tempOrder + " Your order has been confirmed." + " Here are some recomended products based on your purchase: \n" + rec(tempEmail) + " , " + rec(tempEmail))
        await message.channel.send("Confirmation email sent")
        print ("Email Sent") 
      else:
        await message.channel.send(tempEmail + " is not associated with " + tempOrder)


    
    if message.content.startswith('-cancel_order'):
      user_input = message.content.split()
      cancel = False
      tempEmail = user_input[1]
      tempOrder = user_input[2]
      cancel = cancel_order(tempEmail,tempOrder)
      print (cancel)
      if(cancel):
        send_confirmation("testemail19872614@gmail.com" , "Abc123614!" , tempEmail , "Confirmation" , "Hello, " + tempEmail + " your order has been cancelled.")
        await message.channel.send("Your order has been cancelled.")
        print("Email Sent")
      else:
        await message.channel.send("Incorrect email or order.")
 


    if message.content.startswith('-confirm_email'):
      user_input = message.content.split()
      tempEmail = user_input[1]
      send_confirmation("testemail19872614@gmail.com" , "Abc123614!" , tempEmail , "Confirmation" , "Hello, " + tempEmail + "email confirmed.")
      print ("Email Sent") 

    if message.content.startswith('-add_order'):
      user = message.content.split()
      if len(user) != 3:
        await message.channel.send("Invalid Entry Try Again!")
      else:
        email = user[1]
        pid = user[2]
        
        if valid_email(email) and len(pid) == 12:
          add_order(email, pid)
          await message.channel.send("Order Added")
        else:
          await message.channel.send("Invalid Entry!")
    
    if message.content.startswith('-rec'):
      user = message.content.split()
      if user[1] in db['email']:
        recm = rec(str(user[1]))
        await message.channel.send("We reccommend to buy a(n) " + str(recm) + "!")
      else:
        await message.channel.send("Email does not exist!")

    if message.content.startswith('-under'):
      user = message.content.split()
      msg = under(float(user[1]))
      if len(msg) < 1:
        await message.channel.send("No items under " + str(user[1]))
      else:
        await message.channel.send("Items under " + str(user[1]) + "!")
        await message.channel.send(msg)
    #await message.channel.send(len(db))
client.run(os.getenv('TOKEN'))