import TextFeatures as tf
import SpammerFeatures as sp
import csv
import math

#for versioning the output features files
i = 7311
j = 731122

#datasetFile = 'E:/Spam Detection Project on Yelp/Datasets/Balanced Dataset 43000.csv'
datasetFile = 'E:/Spam Detection Project on Yelp/Datasets/Hotels_Dataset_73000.csv'
spammerFeaturesFile = 'E:/Spam Detection Project on Yelp/Features/SpammerFeatures/Spammer Features'+str(i)+'.csv'
outputFilePreparedCosine = 'E:/Spam Detection Project on Yelp/Features/TextFeatures/Prepared Data Cosine.csv'
outputFileTextFeatures = 'E:/Spam Detection Project on Yelp/Features/TextFeatures/Text Features' +str(j)+'.csv'
outputFileCosineSim = 'E:/Spam Detection Project on Yelp/Features/TextFeatures/Cosine Similarity '+str(j)+'.csv'
firstReviewerId = '_0L4WNYQ6f6y6pMYzJ3b9Q'
indexForReviewerId = 1
indexForDate = 7
indexForFirstCount = 16
indexForReviewsCount = 14
indexForHelpfulness = 4
indexForText = 2
indexForlabel = 20
indexForRating = 3
indexForHotelsId = 8


def getSpammerFeatures(datasetFile, spammerFeaturesFile, indexForReviewerId, indexForDate, indexForFirstCount ,
                       indexForReviewsCount, indexForHelpfulness, firstReviewerId):

    MNRFeature = sp.getMNR(datasetFile,indexForReviewerId, indexForDate,firstReviewerId)
    REFeature = sp.getReviewingEarly(datasetFile, indexForFirstCount, indexForReviewsCount)
    AFFeature = sp.getAccountFreshness(datasetFile,indexForReviewerId,indexForDate, firstReviewerId)
    HelpfullFeature = sp.getHelpfulness(datasetFile,indexForReviewerId,indexForHelpfulness,firstReviewerId)
    #CosineFeatureForReviewer = sp.getUserCosFeatures('E:/Spam Detection Project on Yelp/Features/SpammerFeatures/cosineOut.csv', indexForReviewerId,firstReviewerId, indexForText)

    MNRFeatureMapped = mappingToDataset(datasetFile,MNRFeature,indexForReviewerId)
    AFFeatureMapped = mappingToDataset(datasetFile,AFFeature,indexForReviewerId)
    HelpfullFeatureMapped = mappingToDataset(datasetFile,HelpfullFeature,indexForReviewerId)
    #CosineFeatureForReviewerMapped = mappingToDataset(datasetFile, CosineFeatureForReviewer, indexForReviewerId)

    AllSpammerFeatures = [MNRFeatureMapped,AFFeatureMapped,HelpfullFeatureMapped,REFeature]
    writeCSVListOfList(spammerFeaturesFile,AllSpammerFeatures)
#------------------------------------------------------------------------------------------------------
def getCosineSimilarity(datasetFile,outputFilePrepared,outputFileFeature,indexForText):
    preData,text2vector = tf.PrepareForCosine(datasetFile,outputFilePrepared,indexForText)
    cosFeature = []
    for i in range(len(preData)):
        cosineResult = []
        for j in range(len(preData)):
            if (i == j):
                continue
            cosineResult.append(get_cosine(text2vector[i], text2vector[j]))
        cosFeature.append(max(cosineResult))
        print(
            'Done the text number ' + str(i) + ' from ' + str(len(preData)) + ' with result = ' + str(max(cosineResult)))

    write_csv(outputFileFeature, cosFeature)
    print('Done processing')

#-------------------------------------------------------------
#get the text feature and the cosine
def getTextFeatures(datasetFile,textFeaturesFile1, outputFileCosine ,indexForText,indexForlabel):
    textFeaturesFile = open(textFeaturesFile1,'w')
    #avgLenghtDeviation = tf.getAveargeLenghtOfReviews(datasetFile,indexForText,indexForlabel)

    RatingDevFeature = tf.calculateRatingDeviation(datasetFile,indexForReviewerId,indexForRating,indexForHotelsId,firstReviewerId)
    writeCSVListOfListRatingDev('E:\Spam Detection Project on Yelp\Features\TextFeatures\RatingDevFeature.csv',RatingDevFeature)
    #getCosineSimilarity(datasetFile,'E:/Spam Detection Project on Yelp/Features/TextFeatures/prepared Data For Cosine.csv'
    #                   ,outputFileCosine,indexForText)
    #textFeaturesFile.write('Review Lenght Deviation,Url Mention,Avearge Word Lenght,POS Adj,POS Verb,Filtered\n')
    # with open(datasetFile) as csvfile:
    #     CSVReader = csv.reader(csvfile, delimiter=',')
    #     next(csvfile)
    #     for row in CSVReader:
            # adj, verb = tf.get_pos(row[indexForText])
            # textFeaturesFile.write(str(tf.getReviewLenghtDeviation(row[indexForText], avgLenghtDeviation)) + ',' +
            #                        str(tf.is_url(row[indexForText])) + ',' + str(tf.getAveargeWordLenght(row[indexForText])) + ',' +
            #                        str(adj)+ ',' + str(verb)+ ','+str(row[indexForlabel])+'\n')
            # features_file.write(str(ratingDeviation(row[3])))
            # features_file.write(',')
        #textFeaturesFile.close()

#-------------------------------------------------------------

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

#-------------------------------------------------------------
def write_csv(path, result):
    with open(path, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(len(result)):
            csvFile.write(result[i])
            csvFile.write('\n')
    csvFile.close()
#----------------------------------------------------------------
def mappingToDataset(datasetFile,featuresList, indexForReviewerId):

    index = 0
    featuresListMapped = []
    reviewerList = getReviewerList(datasetFile,indexForReviewerId,firstReviewerId)
    with open(datasetFile) as csvfile:
        next(csvfile)
        CSVReader = list(csv.reader(csvfile, delimiter=','))
        for i in range(len(reviewerList)):
            for row in CSVReader[index:]:
                if (row[indexForReviewerId] != reviewerList[i]):
                    break
                featuresListMapped.append(featuresList[i])
                index += 1
    return featuresListMapped
#-------------------------------------------------------------------
def getReviewerList(datasetFile, indexForReviewerId,firstReviewerId):
    reviewerList = []
    with open(datasetFile) as csvfile:
        next(csvfile)
        prevRow = firstReviewerId
        CSVReader = list(csv.reader(csvfile, delimiter=','))
        for row in CSVReader:
            if (row[indexForReviewerId] != prevRow):
                reviewerList.append(prevRow)

            prevRow = row[indexForReviewerId]

        reviewerList.append(prevRow)
    csvfile.close()

    return reviewerList

#-----------------------------------------------------------------------------
def writeCSVListOfList(path, result):
    with open(path, 'w') as csvFile:
        csvFile.write('MNR,AF,Helpfulness,RE\n')
        for j in range(len(result[0])):
            for i in range(len(result)):
                csvFile.write(str(result[i][j]) + ',')
            csvFile.write('\n')
    csvFile.close()
#----------------------------------------------------------------------------
def writeCSVListOfListRatingDev(path, result):
    with open(path, 'w') as csvFile:
        csvFile.write('Rating Deviation\n')
        counter = 0
        for j in range(len(result)):
            for i in range(len(result[counter])):
                csvFile.write(str(result[j][i]) + ',')
                csvFile.write('\n')
            counter += 1
    csvFile.close()

#--------------------------------------------------------------------------------------------------------------------
#running the program
#getSpammerFeatures(datasetFile,spammerFeaturesFile,indexForReviewerId,indexForDate,indexForFirstCount,
 #                                            indexForReviewsCount,indexForHelpfulness,firstReviewerId)

getTextFeatures(datasetFile,outputFileTextFeatures,outputFileCosineSim,indexForText,indexForlabel)




