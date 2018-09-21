import csv
from datetime import datetime
import nltk
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from nltk import word_tokenize
import math
import numpy as np
from scipy import spatial
from nltk.corpus import wordnet as wn
from nltk.metrics import edit_distance
import Lesk as L
import re


#https://xrds.acm.org/blog/2017/07/power-wordnet-use-python/
def MNR(startDate,endDate,numberAllReviews): #Maximum Number Of Reviews
    #we must calculate the above parameters just once then do the function for differnt reviewers
    #think about the time period effect on the result
    NMNOR = 0
    Reviewer_Count = 0
    counter = 0
    features_file = open("temp0.csv", "w")
    features_file.write("Reviewer Id")
    features_file.write(',')
    features_file.write("MNR")
    features_file.write(',')
    features_file.write('\n')
    date_format = "%m/%d/%Y"
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/bal copy.csv') as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in CSVReader:
            if(counter == 0):
                Reviewer_Count += 1
                counter += 1
            elif(counter > 0):
                if(prevRow[1] == row[1]):
                    Reviewer_Count += 1
                elif(prevRow[1] != row[1]):
                    NMNOR = 50 * (Reviewer_Count / numberAllReviews)
                    features_file.write(prevRow[1])
                    features_file.write(',')
                    features_file.write(str(NMNOR))
                    features_file.write(',')
                    features_file.write(str(Reviewer_Count))
                    features_file.write(',')
                    features_file.write(str(numberAllReviews))
                    features_file.write(',')
                    features_file.write('\n')
                    Reviewer_Count = 1
            prevRow = row
    #features_file.close()
    #csvfile.close()
    return 0


#date_f = "%m/%d/%Y"
#a = datetime.strptime('12/6/2004', date_f)
#b = datetime.strptime('10/21/2012', date_f)
#All = 115461

#MNR("7dwh3pL2tbSeSvL0qLzUrw",a,b,All)
#MNR(a,b,All)


###############################################################################
def ReviewingEarly():
    #done
    ROFR = 0
    features_file = open("RE.csv", "w")

    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/balanced_data.csv') as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in CSVReader:
                First_Count = int(row[6])
                Reviews_Count = int(row[7])
                if(Reviews_Count == 0):

                    features_file.write("-1")
                    features_file.write(',')
                    features_file.write('\n')
                else:
                    features_file.write(str(First_Count/Reviews_Count))
                    features_file.write(',')
                    features_file.write('\n')
        #features_file.close()
        #csvfile.close()
    return 0

#ReviewingEarly()
###############################################################################
# Just change the threshold to get the desired output
#method to find the acocunt freshness of the reviewers
def AccountFreshness(): #maybe we can do the min and max dynamicly without list

    # this can be changed
    Threshold = 70
    #####################

    date_format = "%m/%d/%Y"
    Freshness = 0
    Reviewsdate = []
    counter = 0
    features_file = open("temp2.csv", "w")
    features_file.write("Reviewer Id")
    features_file.write(',')
    features_file.write("Account Freshness")
    features_file.write(',')
    features_file.write('\n')
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/balanced_data.csv') as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        reviewerId = '00U0zN1bpBfoRf2iTV7k4g'
        for row in CSVReader:
            if (reviewerId != row[1]):
                endDate =  datetime.strptime(dum, date_format)
                counter = 0
                diff = endDate - firstDate
                if(diff.days > Threshold):
                    features_file.write(reviewerId)
                    features_file.write(',')
                    features_file.write('0')
                    features_file.write(',')
                    features_file.write('\n')
                else:
                    features_file.write(reviewerId)
                    features_file.write(',')
                    features_file.write(str(float(diff.days)/Threshold))
                    features_file.write(',')
                    features_file.write('\n')
                #print(diff)
            if(counter == 0):
                firstDate = datetime.strptime(row[5], date_format)
            dum = row[5]
            counter += 1
            reviewerId = row[1]
        diff = endDate - firstDate
        if (diff.days > Threshold):
            features_file.write(reviewerId)
            features_file.write(',')
            features_file.write('0')
            features_file.write(',')
            features_file.write('\n')
        else:
            features_file.write(reviewerId)
            features_file.write(',')
            features_file.write(str(diff.days / Threshold))
            features_file.write(',')
            features_file.write('\n')
    #features_file.close()
    #csvfile.close()
    return 0




#AccountFreshness()

###############################################################################




def Helpfulness():
    Helpfull = 0
    Useful_Threshold = 4 #determined manualy
    Useful_count = 0
    Helpfull_Count = 0
    Not_Helpfull_Count = 0
    features_file = open("temp3.csv", "w")
    features_file.write("Reviewer Id")
    features_file.write(',')
    features_file.write("Helpfulness")
    features_file.write(',')
    features_file.write('\n')
    counter = 0
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/bal copy.csv') as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in CSVReader:
            if(counter == 0):
                reviewerid = row[1]
                Useful_count = int(row[4])
                if (Useful_count >= Useful_Threshold):
                     Helpfull_Count += 1
                else:
                     Not_Helpfull_Count += 1
                counter += 1
            elif(counter > 0):
                if(prevRow[1] != row[1]):
                    features_file.write(prevRow[1])
                    features_file.write(',')
                    Helpfull = Helpfull_Count / (Helpfull_Count + Not_Helpfull_Count)
                    features_file.write(str(Helpfull))
                    features_file.write(',')
                    features_file.write(str(Helpfull_Count))
                    features_file.write(',')
                    features_file.write(str(Helpfull_Count+Not_Helpfull_Count))
                    features_file.write(',')
                    features_file.write('\n')
                    Helpfull_Count = 0
                    Not_Helpfull_Count = 0
                    Useful_count = int(row[4])
                    if (Useful_count >= Useful_Threshold):
                        Helpfull_Count += 1
                    else:
                        Not_Helpfull_Count += 1
                elif(prevRow[1] == row[1]):
                    Useful_count = int(row[4])
                    if (Useful_count >= Useful_Threshold):
                         Helpfull_Count += 1
                    else:
                         Not_Helpfull_Count += 1
            prevRow = row
    #features_file.close()
    #csvfile.close()
    return 0


#Helpfulness()

##################################################################################################################