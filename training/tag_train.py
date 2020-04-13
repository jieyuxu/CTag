import global_dict
import train
from os import listdir
import csv

# train.init()
# train()

mypath = "/Users/sukiyip/github/IW_JuniorSpring/images/"
sets = listdir(mypath)

for s in sets:
    if s == '.DS_Store':
        continue
    train.train_set(s)

print(global_dict.dict)

remove = []
for t in global_dict.dict.keys():
    if global_dict.dict[t] < 10:
        remove.append(t)

print(remove)

f = open('images.csv')
csv_f = list(csv.reader(f))
new_file = []
for row in csv_f:
  for t in remove:
      if t in row:
          row.remove(t)

# print(csv_f)

with open('better_images.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in csv_f:
        filewriter.writerow(row)
