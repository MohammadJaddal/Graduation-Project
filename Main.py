import csv
import datetime
from  TextFeatures import *
from  SpammerFeatures import *
from  test import *
import time
start_time = time.time()
avgLenghtDeviation = get_avg_len()
print(avgLenghtDeviation)
features_file = open("features_temp.csv", "w")
count = 0
#features_file.write("Avearge Lenght Deviation, URL Mention, Avearge Word Lenght, Review Rating, POS Adj , POS Verb")
#features_file.write('\n')

date_f = "%m/%d/%Y"
a = datetime.datetime.strptime('12/6/2004', date_f)
b = datetime.datetime.strptime('10/21/2012', date_f)
All = 38901
with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/balanced_data.csv') as csvfile:
    CSVReader = csv.reader(csvfile, delimiter=',')
    next(csvfile)
    for row in CSVReader:

        features_file.write(str(get_lenght_deviation(row[2],avgLenghtDeviation)))
        features_file.write(',')
        features_file.write(str(is_url(row[2])))
        features_file.write(',')
        features_file.write(str(get_word_len(row[2])))
        features_file.write(',')
        features_file.write(str(ratingDeviation(row[3])))
        features_file.write(',')
        adj,v = get_pos(row[2])
        features_file.write(str(adj))
        features_file.write(',')
        features_file.write(str(v))
        features_file.write(',')
        features_file.write('\n')
    features_file.close()


features_file1 = open("MNR.csv","w")
features_file2 = open("RE.csv","w")
features_file3 = open("AF.csv","w")
features_file4 = open("Help.csv","w")
MNR(a, b, All)
dup("temp0.csv",features_file1)
ReviewingEarly()
#dup("temp1.csv",features_file2)
AccountFreshness()
dup("temp2.csv",features_file3)
Helpfulness()
dup("temp3.csv",features_file4)


print("--- %s seconds ---" % (time.time() - start_time))

