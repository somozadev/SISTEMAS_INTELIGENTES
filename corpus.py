from numpy import empty, nan
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

import re
# En este bloque se crea la matriz TF-IDF con los stopwords de español


def lectura():
    values = []
    df = pd.read_excel('tweets.xlsx', sheet_name='Search Twitter')
    for i in df.index:
        values.append(df['Text'][i])
    return values


def tokenizado(testStringArray):
    arrayTokenizado = []
    for i in testStringArray:
        aux = word_tokenize(i, language="Spanish")
        arrayTokenizado.append(aux)
        print(aux)
    return arrayTokenizado


# sets every word to .lower in the [][] array
def LowerNTokenize(baseString):

    newBaseString = baseString
    for i in range(len(newBaseString)):
        for j in range(len(newBaseString[i])):
            newBaseString[i][j] = newBaseString[i][j].lower()
    print(newBaseString)
    return newBaseString


def Stemmer(tokenized_text):
    result_txt = [[]]
    stemmer = SnowballStemmer('spanish')
    for k in range(len(tokenized_text)):
        stemmed_txt = [stemmer.stem(i) for i in tokenized_text[k]]
        result_txt.append(stemmed_txt)

    print(result_txt)
    return result_txt


def Criba(text):
    aux = [[]]
    for i in range(len(text)):
         for j in range(len(text[i])):
             text[i][j] = re.findall(r"[\w']+", text[i][j])
 
  
    #aux = filter(None,text)
    aux = [x for x in text if x != []]
    print(aux)
    return aux
    #stop_es = stopwords.words('spanish')
    # tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
    #                        encoding='latin-1', ngram_range=(1, 2), stop_words=stop_es)
    #features = tfidf.fit_transform(df.content).toarray()
    #labels = df.category_id
    # features.shape


class main():
    baseArray = lectura()
    print(baseArray)
    tokenizedArray = tokenizado(baseArray)
    lowerArray = LowerNTokenize(tokenizedArray)
    stemmedString = Stemmer(lowerArray)
    s = Criba(stemmedString)
    # todo : cribar mierda, y pesos tfidf
