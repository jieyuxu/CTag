import csv
from os import listdir
from os.path import isfile, join
from utils.googleapi import *

mypath = "/Users/sukiyip/github/IW_JuniorSpring/images/s1"
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
            filewriter.writerow(a)
        except:
            pass
