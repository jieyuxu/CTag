import csv
from os import listdir
from os.path import isfile, join
from utils.googleapi import *
import global_dict


def train_set(set):
    mypath = "/Users/sukiyip/github/IW_JuniorSpring/images/" + set
    # arr = listdir(filepath)
    # print(arr)

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    with open('images.csv', 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for fname in onlyfiles:
            try:
                path = "gs://erudite-mote-269518-vcm/images/" + fname
                a = [path]

                filepath = mypath + '/' + fname
                big_dict, tag_type = annotate_img_path(filepath)
                tags = big_dict.keys()
                for i in tags:
                    a.append(i)
                    if i in global_dict.dict:
                        global_dict.dict[i] = global_dict.dict[i] + 1
                    else:
                        global_dict.dict[i] = 1
                filewriter.writerow(a)
            except:
                pass

def remove_lows():
    f = open('images.csv')
    csv_f = list(csv.reader(f))

    count = {}
    # get occurances
    for row in csv_f:
        row = row[1:]
        for r in row:
            if r in count:
                count[r] += 1
            else:
                count[r] = 1
    # get things to remove
    remove = []
    for t in count:
        if count[t] < 10:
            remove.append(t)

    print(remove)

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

if __name__ == '__main__':
    remove_lows()
