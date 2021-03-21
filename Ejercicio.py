from os import remove
import re
from sys import __displayhook__
from nltk.corpus.reader import wordlist
from nltk.corpus.reader.verbnet import VerbnetCorpusReader
import pandas as pd
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from scipy import spatial
import operator

nltk.download('stopwords')

# textplob? >> replace

# lee los tweets en el excel y devuelve un array de tweets


def lectura():
    values = []
    df = pd.read_excel('tweets.xlsx', sheet_name='Search Twitter')
    for i in df.index:
        values.append(df['Text'][i])
    return values

# tokeniza el array de tweets


def tokenizado(testStringArray):
    arrayTokenizado = []
    for i in testStringArray:
        aux = word_tokenize(i, language="Spanish")
        arrayTokenizado.append(aux)
    return arrayTokenizado


# sets every word to .lower in the [][] array
def LowerNTokenize(baseString):
    newBaseString = baseString
    for i in range(len(newBaseString)):
        for j in range(len(newBaseString[i])):
            newBaseString[i][j] = newBaseString[i][j].lower()
    return newBaseString

# realiza el stemmer de los tweets tokenizados. también los pasa por una stoplist durante el stemmer


def Stemmer(tokenized_text):
    result_txt = [[]]
    stemmer = SnowballStemmer('spanish')
    for k in range(len(tokenized_text)):
        stemmed_txt = [stemmer.stem(i) for i in tokenized_text[k]]
        result_txt.append(stemmed_txt)
    return result_txt

# limpia los espacios en blanco


def NoEmpty(text):
    nuevo_texto = [[]]
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = re.sub("[^A-Za-z0-9]", '', text[i][j])
        nuevo_texto.append(text[i])
    for i in range(len(text)):
        nuevo_texto[i] = list(filter(None, text[i]))

    nuevonuevo_texto = [[]]
    for i in range(len(text)):
        nuevonuevo_texto_aux = []
        for j in range(len(text[i])):
            if len(text[i][j]) != 0:
                nuevonuevo_texto_aux.append(text[i][j])
        nuevonuevo_texto.append(nuevonuevo_texto_aux)
    nuevonuevo_texto[0].insert(0, 'null')
    nuevonuevo_texto[1].insert(0, 'null')
    nuevonuevo_texto.pop(0)
    nuevonuevo_texto.pop(0)
    return nuevonuevo_texto


def GetTF(word, tweet):
    counter = 0
    for w in tweet:
        if w == word:
            counter += 1

    return counter/len(tweet)


def GetIDF(word, tweets):
    counter = 0
    exists = False
    for tweet in tweets:
        for piece in tweet:
            if word == piece:
                exists = True
        if exists:
            counter += 1
        exists = False

    return math.log10(GetNumberOfDocs(tweets)/counter) 


def GetTFIDF(tf, idf):
    return tf*idf

def GetBagOfWords(noemptyslotsString):
    bagOfWords = []
    for tweet in noemptyslotsString:
        for word in tweet:
                bagOfWords.append(word)
    aux = set()
    result = []
    for word in bagOfWords:
        if word not in aux:
            aux.add(word)
            result.append(word)
    # print("BAG: " + str(bagOfWords))
    # print("BAG: " + str(result))
    return result

def GetBagOfWordsTFIDF(noemptyslotsString, simpleBagOfWords):

    BagOfVectorWords = []

    for word in simpleBagOfWords:
        idf = GetIDF(word, noemptyslotsString)
        tfidfVector = []
        for tweet in noemptyslotsString:
            tf = GetTF(word, tweet)
            tfidf = GetTFIDF(tf, idf)
            tfidfVector.append(tfidf)
        BagOfVectorWords.append(VectorWord(word,tfidfVector))

    return BagOfVectorWords

def GetDocsOfWords(numberOfDocs,bagOfWords):
    vectorDocs = []
    counter = 0
    for doc in range(numberOfDocs):
        vectorDocsValue = []
        for vector in bagOfWords:
            vectorDocsValue.append(vector.tfidfList[counter])
        counter += 1
        vectorDocs.append(vectorDocsValue)
    return vectorDocs

def GetCosines(docsOfWords, baseArray):
    cosinesSimilarities = []
    for i in range(len(docsOfWords)-1): #se pone -1 para no incluir la propia query
        cosineSimilarity = 1 - spatial.distance.cosine(docsOfWords[i],docsOfWords[len(docsOfWords)-1])
        cosinesSimilarities.append(CosineSim(cosineSimilarity,i))

    sortedCosines = sorted(cosinesSimilarities, key = operator.attrgetter('cosine'))
    print("5º" + "\n cosine:" + str(sortedCosines[147].cosine) + "\n tweet id:" + str(sortedCosines[147].tweetNumber) + "\n tweet:" + str(baseArray[sortedCosines[147].tweetNumber]))
    print("4º" + "\n cosine:" + str(sortedCosines[148].cosine) + "\n tweet id:" + str(sortedCosines[148].tweetNumber) + "\n tweet:" + str(baseArray[sortedCosines[148].tweetNumber]))
    print("3º" + "\n cosine:" + str(sortedCosines[149].cosine) + "\n tweet id:" + str(sortedCosines[149].tweetNumber) + "\n tweet:" + str(baseArray[sortedCosines[149].tweetNumber]))
    print("2º" + "\n cosine:" + str(sortedCosines[150].cosine) + "\n tweet id:" + str(sortedCosines[150].tweetNumber) + "\n tweet:" + str(baseArray[sortedCosines[150].tweetNumber]))
    print("1º" + "\n cosine:" + str(sortedCosines[151].cosine) + "\n tweet id:" + str(sortedCosines[151].tweetNumber) + "\n tweet:" + str(baseArray[sortedCosines[151].tweetNumber]))

    return sortedCosines

<<<<<<< HEAD
def analisisSentimiento(frase):

    analysis = TextBlob(frase)
    language = analysis.detect_language()
    if language == 'en':
        analysis_ready = analysis
    else:
        analysis_ready = analysis.translate(to='en')
                
    if analysis_ready.sentiment.polarity > 0: 
        return("positive")
    elif analysis_ready.sentiment.polarity == 0: 
        return("neutral")
    else: 
        return("negative")
=======
>>>>>>> parent of 78c1797 (Merge branch 'master' of https://github.com/somozadev/SISTEMAS_INTELIGENTES)

def GetNumberOfDocs(text):
    number = 0
    for i in range(len(text)):
        number += 1
    return number

class VectorWord:
    def __init__(self, word, tfidfList):
        self.word = word
        self.tfidfList = tfidfList
class VectorDoc:
    def __init__(self, tfidfList):
        self.tfidfList = tfidfList
class CosineSim:
    def __init__(self, cosine, tweetNumber):
        self.cosine = cosine
        self.tweetNumber = tweetNumber

class main():

tokenizedArray = tokenizado(baseArray)
print(tokenizedArray)

'''
    baseArray = lectura()
    # print(baseArray) '''
'''
    query = (str(input("Write query: ")))
    baseArray.append(query) 


    numberOfDocs = GetNumberOfDocs(baseArray)
    # print(numberOfDocs)
    

    
    lowerArray = LowerNTokenize(tokenizedArray)
    # print(lowerArray)
    stemmedString = Stemmer(lowerArray)
    # print(stemmedString)
    noemptyslotsString = NoEmpty(stemmedString)
    # print(noemptyslotsString)
    simpleBagOfWords = GetBagOfWords(noemptyslotsString) 
    # print(simpleBagOfWords)
    bagOfWords = GetBagOfWordsTFIDF(noemptyslotsString, simpleBagOfWords)
    # for vector in bagOfWords:
    #     print(str(vector.word) + ":" + str(vector.tfidfList))
    docsOfWords = GetDocsOfWords(numberOfDocs,bagOfWords)
    # for vector in docsOfWords:
    #     print(str(vector.tfidfList))
    cosinesSimilarities = GetCosines(docsOfWords, baseArray)
'''

   

    