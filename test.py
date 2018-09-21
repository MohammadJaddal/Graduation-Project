import csv
from  SpammerFeatures import *
import datetime

def dup(fileRead,fileWrite):

    index = 0
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/balanced_data.csv') as csvfile:
        next(csvfile)
        CSVReader = list(csv.reader(csvfile, delimiter=','))
        with open(fileRead) as fe:
              feReader = csv.reader(fe, delimiter=',')
              next(fe)
              for row in feReader:
                    for row_csv in CSVReader[index:]:
                        if(row[0] != row_csv[1]):
                            break
                        fileWrite.write(row[1])
                        fileWrite.write(',')
                        fileWrite.write('\n')
                        index += 1

def merge():
    import time
    start_time = time.time()
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/MNR.csv') as MNRfile:
        MNRReader = csv.reader(MNRfile, delimiter=',')
        with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/RE.csv') as REfile:
            REReader = csv.reader(REfile, delimiter=',')
            with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/features_temp.csv') as f_tempfile:
                f_tempReader = csv.reader(f_tempfile, delimiter=',')
                with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/AF.csv') as AFfile:
                    AFReader = csv.reader(AFfile, delimiter=',')
                    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/Help.csv') as Helpfile:
                        HelpReader = csv.reader(Helpfile, delimiter=',')
                        features_final = open("Final_features.csv", "w")
                        features_final.write("Avearge Lenght Deviation, URL Mention, Avearge Word Lenght, Review Rating, POS Adj , POS Verb, MNR, Reviewing Early, Helpfull, Account Freshness ")
                        features_final.write(',')
                        features_final.write('\n')
                        index = 0


                        for (row1, row2, row3, row4, row5) in zip(f_tempReader, MNRReader, REReader, HelpReader, AFReader):
                            features_final.write(row1[0] + "," + row1[1] + "," + row1[2] + "," + row1[3] + "," + row1[4] + "," + row1[5])
                            features_final.write("," + row2[0] + "," + row3[0] + "," + row4[0] + "," + row5[0])
                            features_final.write('\n')

    features_final.close()
    Helpfile.close()
    MNRfile.close()
    AFfile.close()
    f_tempfile.close()
    REfile.close()

    print("--- %s seconds ---" % (time.time() - start_time))

merge()