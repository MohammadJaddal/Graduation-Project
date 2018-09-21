import nltk
import csv
import re
import math
import sys
from collections import Counter
from nltk.corpus import stopwords
from stemming.porter2 import stem
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
import numpy as np
from scipy import spatial
from nltk.metrics import edit_distance
import Lesk as L
import re


#####################################################################################################################
def get_avg_rate(id):
    length=0
    ext_flag=0
    lower=1
    upper=5
    count=0
    rating=0
    with open('C:/Users/admin/PycharmProjects/Graduation-Project/Output.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(id==row[1]):
                rating+=int(row[3])
                count+=1

    result=rating/count
    if (result > upper or result < lower):
        ext_flag = 1
    else:
        ext_flag = 0
    #print(ext_flag)
    #print(rating)
    #print(count)
    #print(result)


    return result
    #return ext_flag

def ratingDeviation(rating):
    return int(rating)/5

#######################################################################################################################

#def get_pos(message):
#    review_tokenized = []
#    message=str(message)
#    lmt = WordNetLemmatizer()
#    tokenize_words = word_tokenize(message.lower(),language='english')
#    pos_word = pos_tag(tokenize_words)
#    tokenize_words = ["_".join([lmt.lemmatize(i[0]),i[1]]) for i in pos_word if (i[0] not in stopwords.words("english") and len(i[0]) > 2)]
#    review_tokenized.append(tokenize_words)
#    print(review_tokenized)


    #message= review_tokenized


def get_pos(message):
    message=str(message).lower()

    tokenized = word_tokenize(message)
    tagged = pos_tag(tokenized)
    dev_j=0
    dev_n=0
    count=0
    #print(tagged)
    for i in tagged:
        if i[1]=="JJ": # NN for nouns, RB for adverbs, JJ for adjective, VBP for verbs....
            #print(i)
            count+=1
    if len(tagged)!=0:
        dev_j=count/len(tagged)

    count=0;
    for i in tagged:
        if i[1] == "VB":  # NN for nouns, RB for adverbs, JJ for adjective , VBP for verbs....
            #print(i)
            count += 1
    if len(tagged)!=0:
        dev_n=count/len(tagged)

    #print(dev)
    return dev_j,dev_n
    #print(len(tagged))


#print(get_pos("this is a sample to test test pos taggers bad good"))

#####################################################################################################################
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


def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(text)
    return Counter(words)


def get_result(content_a, content_b):
    text1 = content_a
    text2 = content_b

    vector1 = text_to_vector(text1)
    vector2 = text_to_vector(text2)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result


def find_cos(statment1,statment2):
    statment1=statment1.lower();
    statment2=statment2.lower();
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



    statment1 = re.sub(r'[^\w\s]','',statment1).replace('  ',' ')
    statment2 = re.sub(r'[^\w\s]','',statment2).replace('  ',' ')




    #print(statment1)

    #print(statment2)

    return get_result(statment1,statment2)




#start = time.time()

#print(find_cos("I came to Chicago on business and was initially supposed to stay downtown; however a colleague recommended this hotel--and I am so glad that they did! The attention to detail and finishing touches in my room are what made this hotel feel like home. Staying in a smaller hotel allowed me to connect with the local Chicago vibe while simultaneously enjoying exquisite service from the staff at a fraction of what it might cost to stay in a Magnificent Mile high-rise. Considering the quality ambiance and charm of this hidden Chicago treasure it made my trip a memorable experience. Not only was I able to secure a bike rental to avoid the high cost of renting a car but I also was directed to some of the local galleries in the West Loop by the friendly staff members.","I still love this place but the took Mu Shu off the menu. Â I am deeply saddened. Show owner comment Â»"))

#print(time.time()-start)



#####################################################################################################################
#done
def get_lenght_deviation(message,aveargeLenght):

    threshold = 0.5 #could be changed
    my_flag=0
    if(aveargeLenght == 0):
        return -1
    dev=len(message)/aveargeLenght

    #if(dev<0.5):
    #    my_flag=1
    #else:
    #    my_flag=0

    return dev
#we must edit to return dev
#####################################################################################################################
#done
def get_avg_len():
    length=0
    count=0
    with open('D:/books and outline/5-Fifth-year-1st_semester/Graduation Project/rrr/Output10.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            length+=len(row[2])
            count+=1
    if(count == 0):
        return -1
    result=length/count
    return result


#####################################################################################################################
#this feature checks for a url other than yelp.com
#done and put it in the loop
def is_url(message):
    my_flag=0
    if(message.__contains__(".[a-z]/[c o m][ /]")):
        return 1
    if((".com") in message):
        if(message.count("yelp.com") == message.count(".com")):
            return 0
        else:
            return 1

    return my_flag


#####################################################################################################################
#done
def get_word_len(message):
    my_flag = 0
    number_of_words=0

    count = len(re.findall(r'\w+', message))
    if count == 0:
        return -1
    avg_len=len(message.replace(" ",""))/count
    #if(avg_len>6 or avg_len <4):
     #   my_flag=1
    #else:
     #   my_flag=0
    return avg_len

#print(get_word_len("maod mohanad nn mod mohanad mohanad mohanad mohanad mohanad mohanad mohanad mohanad mohanad"))


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

    # print R

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
sen1 = "good work"
sen2 = "good work"
#print("semantic similarity between the two sentences : ")
#print(semanticSimilarity(sen1,sen2))



#####################################################################################################################



#####################################################################################################################