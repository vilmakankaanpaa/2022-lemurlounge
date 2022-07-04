from itertools import permutations
import random
from datetime import datetime, timedelta, date

# Used this file to get exactly right amount of each stimuli to be varied daily

fileName = 'contentOrder.txt'

def createNewOrder(
  content=['rain','traffic','music','zen','whitenoise'], 
  startDate='2022-07-01', 
  contentDays=7):
  
  # stimuli: list of the stimuli content
  # startDate: start date of the study (e.g. '2022-07-01')

  perm = permutations(content)
  perm = list(perm)

  orderlist = []

  for i in range(0,contentDays-1):
    choice = random.choice(perm)
    for stimulus in choice:
      orderlist.append(stimulus)

  alternatedates = {}

  startDate = date.fromisoformat(startDate)

  for i in range(0,len(orderlist)-1):
    newDate = startDate + timedelta(days=i)
    alternatedates.update({ newDate : orderlist[i] })

  f = open(fileName,'w')
  for key in alternatedates:
    f.write(key.isoformat() + " " + alternatedates[key]+ "\n")
  f.close()

def getDictionary():

  f = open(fileName,'r')
  results = f.readlines()
  f.close()

  dict = {}

  for line in results:
    print(line)
    dict.update({line[0:10] : line[11:-1]}) # -1 so that the line divider \n is not read too

  # for key in dict:
  #   print(key, dict[key])

  return dict