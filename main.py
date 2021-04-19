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
def add_order(email,id,price):
  current = user_order(email,id,price)
  users[current.email] = current

# Recs an item based on past orders
def rec(email,order):

  tempOrder = int (order)


  orders = ['food','car_stuff','clothes','toys','misc']

  max_order = ''
  
  random_num = tempOrder

  if random_num == 0:
    max_order = 'food'
  elif random_num == 1:
    max_order = 'car_stuff'
  elif random_num == 2:
    max_order = 'clothes'
  elif random_num == 3:
    max_order = 'toys'
  else:
    max_order = 'misc'

  if max_order == 'food':
    rand_num = random.randint(0,len(food)-1)
    return food[rand_num]
  elif max_order == 'car_stuff':
    rand_num = random.randint(0,len(car_stuff)-1)
    return car_stuff[rand_num]
  elif max_order == 'clothes':
    rand_num = random.randint(0,len(clothes)-1)
    return car_stuff[rand_num]
  elif max_order == 'toys':
    rand_num = random.randint(0,len(toys)-1)
    return toys[rand_num]
  elif max_order == 'misc':
    rand_num = random.randint(0,len(misc)-1)
    return misc[rand_num]
  else:
    return False
  
# returns all items under given price
def under(price):
  under_price = []
  for i in users:
    if users[i].price < price:
      under_price.append(users[i].id1)
  for i in range(len(under_price)):
    first = under_price[i][0]
    under_price.insert(i,items[str(first)])
    under_price.pop(-1)

  return under_price



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
      send_confirmation("testemail19872614@gmail.com" , "Abc123614!" , tempEmail , "Confirmation" , "Hello, " + tempEmail + " " + tempOrder + " Your order has been confirmed." + " here are some recomended products based on your purchase: \n" + rec(tempEmail,tempOrder) + " , " + rec(tempEmail, tempOrder))
      await message.channel.send("Confirmation email sent")
      print ("Email Sent") 

    if message.content.startswith('-confirm_email'):
      user_input = message.content.split()
      tempEmail = user_input[1]
      send_confirmation("testemail19872614@gmail.com" , "Abc123614!" , tempEmail , "Confirmation" , "Hello, " + tempEmail + "email confirmed.")
      print ("Email Sent") 

    if message.content.startswith('-add_order'):
      user = message.content.split()
      if len(user) != 4:
        await message.channel.send("Invalid Entry Try Again!")
      else:
        email = user[1]
        pid = user[2]
        cost = user[3]
        cost = float(cost)
        if valid_email(email) and len(pid) == 12 and type(cost) == float and cost > 0:
          add_order(email, pid, cost)
          await message.channel.send("Order Added")
        else:
          await message.channel.send("Invalid Entry!")
    
    if message.content.startswith('-rec'):
      user = message.content.split()
      if user[1] in db['email']:
        op = rec(user[1])
        await message.channel.send("We recommend that you buy " + str(op) + "(s)!")
      else:
        await message.channel.send("Invalid Entry")

    if message.content.startswith('-under'):
      user = message.content.split()
      await message.channel.send("Under $" + str(user[1]) + "!")
      if len(under(str[user[1]])) < 1:
        await message.channel.send("No items under " + str(user[1]))
      else:
        await message.channel.send(under(float(user[1])))
    #await message.channel.send(len(db))
client.run(os.getenv('TOKEN'))