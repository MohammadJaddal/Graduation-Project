import nltk
import csv
import math
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
import numpy as np
from nltk.metrics import edit_distance
import Lesk as L
import re


#----------------------------------------------------------------------------------------------------------
#gets the pos for adj, and noun of the text provided
def get_pos(message):
    message=str(message).lower()

    tokenized = word_tokenize(message)
    tagged = pos_tag(tokenized)
    dev_j=0
    dev_n=0
    count=0
    for i in tagged:
        if i[1]=="JJ": # NN for nouns, RB for adverbs, JJ for adjective, VBP for verbs....
            count+=1
    if len(tagged)!=0:
        dev_j=count/len(tagged)

    count=0;
    for i in tagged:
        if i[1] == "VB":  # NN for nouns, RB for adverbs, JJ for adjective , VBP for verbs....
            count += 1
    if len(tagged)!=0:
        dev_n=count/len(tagged)

    return dev_j,dev_n


#----------------------------------------------------------------------------------------------------------
#return the difference betwwen the lenght of the review from the avearge lenght of the dataset
def getReviewLenghtDeviation(message,aveargeLenght):

    if(aveargeLenght == 0):
        return -1
    deviation = abs(len(message)-aveargeLenght)

    return deviation
#------------------------------------------------------------------------------------------------------------------
#return the avearge lenght of chars in the dataset for non spam
def getAveargeLenghtOfReviews(datasetFile, indexForText, indexForLabel):
    count = 0
    sum = 0
    with open(datasetFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(row[indexForLabel] == '0'):
                length = len(row[indexForText])
                sum += length
                count +=1

    if(count == 0):
        return 0
    avg = sum/count
    return avg

#---------------------------------------------------------------------------------------------------------------
#this feature checks for a url other than yelp.com
def is_url(message):

    numberOfURL = 0
    if(message.__contains__(".[a-z]/[c o m][ /]")):
        numberOfURL += message.count(".[a-z]/[c o m][ /]")
    if((".com") in message):
        if(message.count("yelp.com") == message.count(".com")):
            return 0
        else:
            numberOfURL += message.count(".com")
    return numberOfURL
#----------------------------------------------------------------------------------------------------------------
#This feature return always between 4 and 6 gaussian distrbution
def getAveargeWordLenght(message):

    count = len(re.findall(r'\w+', message))
    if count == 0:
        return -1
    avg_len=len(message.replace(" ",""))/count

    return avg_len

#####################################################################################################################
#semantic feature
def path(set1, set2):
    return wn.path_similarity(set1, set2)


def wup(set1, set2):
    return wn.wup_similarity(set1, set2)


def edit(word1, word2):
    if float(edit_distance(word1, word2)) == 0.0:
        return 0.0
    return 1.0 / float(edit_distance(word1, word2))

def stemmer(tag_q1, tag_q2):
    """
        tag_q = tagged lists. Function returns a stemmed list.
    """
    st = nltk.stemmer.PorterStemmer()
    stem_q1 = []
    stem_q2 = []

    for token in tag_q1:
        stem_q1.append(st.stem(token))

    for token in tag_q2:
        stem_q2.append(st.stem(token))

    return stem_q1, stem_q2

def tokenize(s1, s2):
    """
        s1 and s2 are sentences/questions. Function returns a list of tokens for both.
    """
    return word_tokenize(s1), word_tokenize(s2)


def posTag(q1, q2):
    """
        q1 and q2 are lists. Function returns a list of POS tagged tokens for both.
    """
    return nltk.pos_tag(q1), nltk.pos_tag(q2)
def WordNet(review1,review2):

    tok1 = tokenize(review1,review2)
    posTagged = posTag(tok1[0],tok1[1])
    #print(posTagged)


def computePath(q1, q2):

    R = np.zeros((len(q1), len(q2)))

    for i in range(len(q1)):
        for j in range(len(q2)):
            if q1[i][1] == None or q2[j][1] == None:
                sim = edit(q1[i][0], q2[j][0])
            else:
                sim = path(wn.synset(q1[i][1]), wn.synset(q2[j][1]))

            if sim == None:
                sim = edit(q1[i][0], q2[j][0])

            R[i, j] = sim

    # print R

    return R

def computeWup(q1, q2):

    R = np.zeros((len(q1), len(q2)))

    for i in range(len(q1)):
        for j in range(len(q2)):
            if q1[i][1] == None or q2[j][1] == None:
                sim = edit(q1[i][0], q2[j][0])
            else:
                sim = wup(wn.synset(q1[i][1]), wn.synset(q2[j][1]))

            if sim == None:
                sim = edit(q1[i][0], q2[j][0])

            R[i, j] = sim
    return R


def overallSim(q1, q2, R):
    sum_X = 0.0
    sum_Y = 0.0

    for i in range(len(q1)):
        max_i = 0.0
        for j in range(len(q2)):
            if R[i, j] > max_i:
                max_i = R[i, j]
        sum_X += max_i

    for i in range(len(q1)):
        max_j = 0.0
        for j in range(len(q2)):
            if R[i, j] > max_j:
                max_j = R[i, j]
        sum_Y += max_j

    if (float(len(q1)) + float(len(q2))) == 0.0:
        return 0.0

    overall = (sum_X + sum_Y) / ( (float(len(q1)) + float(len(q2))))
    #print("OverAll output = ",overall)
    return overall

def semanticSimilarity(q1, q2):

    tokens_q1, tokens_q2 = tokenize(q1, q2)
    # stem_q1, stem_q2 = stemmer(tokens_q1, tokens_q2)
    tag_q1, tag_q2 = posTag(tokens_q1, tokens_q2)

    sentence = []
    for i, word in enumerate(tag_q1):
        if 'NN' in word[1] or 'JJ' in word[1] or 'VB' in word[1]:
            sentence.append(word[0])

    sense1 = L.Lesk(sentence)
    sentence1Means = []
    for word in sentence:
        sentence1Means.append(sense1.lesk(word, sentence))

    sentence = []
    for i, word in enumerate(tag_q2):
        if 'NN' in word[1] or 'JJ' in word[1] or 'VB' in word[1]:
            sentence.append(word[0])

    sense2 = L.Lesk(sentence)
    sentence2Means = []
    for word in sentence:
        sentence2Means.append(sense2.lesk(word, sentence))
    # for i, word in enumerate(sentence1Means):
    #     print sentence1Means[i][0], sentence2Means[i][0]

    R1 = computePath(sentence1Means, sentence2Means)
    R2 = computeWup(sentence1Means, sentence2Means)

    R = (R1 + R2) / 2

    # print R

    return overallSim(sentence1Means, sentence2Means, R)



STOP_WORDS = nltk.corpus.stopwords.words()
def clean_sentence(val):
    "remove chars that are not letters or numbers, downcase, then remove stop words"
    regex = re.compile('([^\s\w]|_)+')
    sentence = regex.sub('', val).lower()
    sentence = sentence.split(" ")

    for word in list(sentence):
        if word in STOP_WORDS:
            sentence.remove(word)

    sentence = " ".join(sentence)
    return sentence


#WordNet("I went to the supermarket","he will move to another place")
#sen1 = "good work"
#sen2 = "good work"
#print("semantic similarity between the two sentences : ")
#print(semanticSimilarity(sen1,sen2))

#----------------------------------------------------------------------------------------------------------
#gets the cosine similarity for 2 sentences

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
#----------------------------------------------------------------------------------------------------------

def get_result(content_a, content_b):
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result
#----------------------------------------------------------------------------------------------------------

def find_cos(statment1,statment2):
    statment1 = statment1.lower();
    statment2 = statment2.lower();
    word_tokens = word_tokenize(statment1)
    word_tokens2 = word_tokenize(statment2)
    stop_words = set(stopwords.words('english'))
    snow = nltk.SnowballStemmer('english')
    filtered_sentence1 = [w for w in word_tokens if not w in stop_words]
    filtered_sentence1 = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence1.append(w)

    filtered_sentence2 = [w for w in word_tokens2 if not w in stop_words]
    filtered_sentence2 = []

    for w in word_tokens2:
        if w not in stop_words:
            filtered_sentence2.append(w)

    statment1=''
    for word in filtered_sentence1:
        statment1+=snow.stem(word)+' '
    statment2=''
    for word in filtered_sentence2:
        statment2 += snow.stem(word)+' '

    statment1 = re.sub(r'[^\w\s]','', statment1).replace('  ',' ')
    statment2 = re.sub(r'[^\w\s]','', statment2).replace('  ',' ')

    return get_result(statment1, statment2)
#----------------------------------------------------------------------------------------------------------

def preProcessing(statement):
    statement1 = statement.lower();
    word_tokens = word_tokenize(statement1)
    stop_words = set(stopwords.words('english'))
    snow = nltk.SnowballStemmer('english')
    filtered_sentence1 = [w for w in word_tokens if not w in stop_words]

    FinalStatement = ''
    for word in filtered_sentence1:
        FinalStatement += snow.stem(word) + ' '

    FinalStatement = re.sub(r'[^\w\s]', '', FinalStatement).replace('  ', ' ')

    return FinalStatement

#----------------------------------------------------------------------------------------------------------
def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)

#----------------------------------------------------------------------------------------------------------

#prepare the data for get cosine similarity
def PrepareForCosine(datasetFile,outputFile1,indexForText):
    outputFile = open(outputFile1,'w')
    text2vector = []
    preData = []

    with open(datasetFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            pre = preProcessing(row[indexForText])
            outputFile.write(pre)
            outputFile.write('\n')
            preData.append(pre)
            text2vector.append(text_to_vector(pre))
    return preData, text2vector
#----------------------------------------------------------------------------------------------------------
