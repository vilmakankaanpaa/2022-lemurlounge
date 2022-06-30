from itertools import permutations
import random
from datetime import datetime, timedelta, date

# Used this file to get exactly right amount of each stimuli to be varied daily

# stimuli: list of the stimuli content
stimuli = ['rain','traffic','music','zen','whitenoise']

# startDate: start date of the study (e.g. '2022-07-01')
startDate = '2022-07-01'

perm = permutations(stimuli)
perm = list(perm)

orderlist = []

for i in range(0,6):
  choice = random.choice(perm)
  print(choice)
  for stimulus in choice:
    orderlist.append(stimulus)

print()
print('Final order:')
print(orderlist)

alternatedates = {}

startDate = date.fromisoformat(startDate)

for i in range(0,len(orderlist)-1):
  newDate = startDate + timedelta(days=i)
  alternatedates.update({ newDate : orderlist[i] })

print()
print('alternating audio:')
print()

for key in alternatedates:
  print(key, alternatedates[key])
