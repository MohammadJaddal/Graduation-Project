import csv
from datetime import datetime


#https://xrds.acm.org/blog/2017/07/power-wordnet-use-python/
#--------------------------------------------------------------------------------------------
#takes a list of dates and return the max occurance of the date
import TextFeatures


def ReviewerMNR(reviewerDates):
    mnrCounter = []
    counter = 0
    for i in range(len(reviewerDates)):
        counter = 0
        for j in range(len(reviewerDates)):
            if(reviewerDates[i] == reviewerDates[j]):
                counter += 1
        mnrCounter.append(counter)
    return max(mnrCounter)

#get the MNR for all reviewers
def getMNR(datasetFile, indexForReviewerId, indexForDates,firstReviewerId):

    MNRFeature = []
    reviewerDates = []
    with open(datasetFile) as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        prevRow = firstReviewerId
        for row in CSVReader:
            if (row[indexForReviewerId] == prevRow):
                reviewerDates.append(row[indexForDates])

            elif (row[indexForReviewerId] != prevRow):
                MNRFeature.append(ReviewerMNR(reviewerDates))
                reviewerDates.clear()
                reviewerDates.append(row[indexForDates])

            prevRow = row[indexForReviewerId]
        MNRFeature.append(ReviewerMNR(reviewerDates))
    csvfile.close()
    return MNRFeature

#------------------------------------------------------------------------------------------------
#returned mapped RE feature
def getReviewingEarly(datasetFile,indexForFirstCount, indexForReviewsCount):

    REFeature = []
    with open(datasetFile) as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        for row in CSVReader:
            First_Count = int(row[indexForFirstCount])
            Reviews_Count = int(row[indexForReviewsCount])
            if(Reviews_Count == 0):
                REFeature.append(-1)
            else:
                REFeature.append(First_Count/Reviews_Count)
    return REFeature

#-------------------------------------------------------------------------------------------------------
#Calculates the account freshness for the reviewers
def getAccountFreshness(datasetFile, indexForReviewerId, indexForDate,firstReviewerId):

    date_format = "%m/%d/%Y"
    counter = 0
    AFFeature = []
    with open(datasetFile) as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        reviewerId = firstReviewerId
        for row in CSVReader:
            if (reviewerId != row[indexForReviewerId]):
                endDate =  datetime.strptime(dum, date_format)
                counter = 0
                diff = endDate - firstDate
                AFFeature.append(int(diff.days))

            if(counter == 0):
                firstDate = datetime.strptime(row[indexForDate], date_format)
            dum = row[indexForDate]
            counter += 1
            reviewerId = row[indexForReviewerId]
        diff = endDate - firstDate
        AFFeature.append(int(diff.days))
    csvfile.close()
    return AFFeature

#-------------------------------------------------------------------------------------------
#gets the helpfullness feature for the reviewer
def getHelpfulness(datasetFile, indexForReviewerId, indexForHelpfulness,firstReviewerId):

    HelpfullFeature = []
    Helpfull_Count = 0
    count_reviewer = 0
    with open(datasetFile) as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        prevRow = firstReviewerId
        for row in CSVReader:
            if (row[indexForReviewerId] == prevRow):
                Helpfull_Count += int(row[indexForHelpfulness])
                count_reviewer += 1

            elif (row[indexForReviewerId] != prevRow):
                HelpfullFeature.append(Helpfull_Count / count_reviewer)
                Helpfull_Count = int(row[indexForHelpfulness])
                count_reviewer = 1
            prevRow = row[indexForReviewerId]
        HelpfullFeature.append(Helpfull_Count / count_reviewer)
    csvfile.close()

    return HelpfullFeature

#----------------------------------------------------------------------------------------------------------------
#gets the avearge rating for specific reviewer
def getAveargeRateingForReviewer(datasetFile,ReviewerId, indexforRating):
    count=0
    rating=0
    with open(datasetFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(id==row[ReviewerId]):
                rating+=int(row[indexforRating])
                count+=1

    result=rating/count
    return result

#------------------------------------------------------------------

def getAveargeRatingOfNonSpam(datasetFile, indexForRating, indexForLabel):
    count = 0
    sum = 0
    with open(datasetFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(row[indexForLabel] == '1'):
                sum += int(row[indexForRating])
                count +=1

    if(count == 0):
        return 0
    avg = sum/count
    return avg
#print(getAveargeRatingOfNonSpam('E:/Spam Detection Project on Yelp/Datasets/Balanced Dataset 43000.csv',3, 8))

#---------------------------------------------------------------------------------------------------------------
#Cosine simliarity for reviewer
def getReviewerCosineSimliarity(userReviews):
    max = 0
    index1 = 0
    index2 = 0
    text2vector = []
    for review in userReviews:
        pre = TextFeatures.preProcessing(review)
        text2vector.append(TextFeatures.text_to_vector(pre))

    for review1 in text2vector:
        index1 += 1
        for review2 in text2vector:
            index2 += 1
            if index1 != index2:
                current = TextFeatures.get_cosine(review1,review2)
                if (current > max ):
                    max=current
        index2 = 0
    return max


def getUserCosFeatures(datasetFile, indexForReviewerId, firstReviewerId, indexForText):
    CosineFeature = []
    counter = 0
    max = 0
    userReviews = []

    with open(datasetFile) as csvfile:
        CSVReader = csv.reader(csvfile, delimiter=',')
        next(csvfile)
        reviewerId = firstReviewerId
        for row in CSVReader:
            if(reviewerId == row[indexForReviewerId]):
                userReviews.append(row[indexForText])
            else:
                feature = getReviewerCosineSimliarity(userReviews)
                CosineFeature.append(feature)
                counter += 1
                userReviews.clear()
                userReviews.append(row[indexForText])
            reviewerId = row[indexForReviewerId]
    feature = getReviewerCosineSimliarity(userReviews)
    CosineFeature.append(feature)
    print('len is :',len(CosineFeature))
    csvfile.close()
    return CosineFeature

