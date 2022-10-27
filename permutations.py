from itertools import permutations
import random
import datetime

fileName = 'contentorder.txt'

def newOrder(
  content=['a','b','c'], 
  startDate='2022-07-01', 
  occurrences=7,
  cycle=1):
  
  # content: list of the content to be alternating
  # startDate: start date of the study (e.g. '2022-07-01')
  # occurrences: how many times a single content should occur during 
  #              the span of the study
  # cycle: how many days a content should be played in a row 
  #              (e.g. 3 days of file A, 3 dyas of file B, etc.)

  perm = permutations(content) # create all possible permutations with content
  perm = list(perm)

  orderlist = [] 

  # Pick random permutations from all options and save as 
  # single continuous list
  for i in range(0,occurrences-1):
    choice = random.choice(perm)
    for stimulus in choice:
      orderlist.append(stimulus)

  alternatedates = {}
  date = datetime.date.fromisoformat(startDate)

  # Starting from the given date, assign starting dates for each 
  # occurrence of contents
  for i in range(0, len(orderlist)-1):
    date += datetime.timedelta(days=cycle)
    alternatedates.update({ date : orderlist[i] })

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
    dict.update({line[0:10] : line[11:-1]}) # -1 so that the line divider \n is left behind.

  # for key in dict:
  #   print(key, dict[key])

  return dict