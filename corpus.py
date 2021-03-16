import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
import pandas as pd
import math
import nltk
nltk.download('stopwords')
# textplob? >> replace
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
        # print(aux)
    return arrayTokenizado


# sets every word to .lower in the [][] array
def LowerNTokenize(baseString):

    newBaseString = baseString
    for i in range(len(newBaseString)):
        for j in range(len(newBaseString[i])):
            newBaseString[i][j] = newBaseString[i][j].lower()
    # print(newBaseString)
    return newBaseString


def Stemmer(tokenized_text):
    result_txt = [[]]
    stemmer = SnowballStemmer('spanish')
    for k in range(len(tokenized_text)):
        stemmed_txt = [stemmer.stem(i) for i in tokenized_text[k]]
        result_txt.append(stemmed_txt)

    # print(result_txt)
    return result_txt

# limpia los espacios en blanco


def NoEmpty(text):
    nuevo_texto = [[]]
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = re.sub("[^A-Za-z0-9]", '', text[i][j])

        # text[i][j] = re.findall( ' ', text[i][j])
        nuevo_texto.append(text[i])

    for i in range(len(text)):
        nuevo_texto[i] = list(filter(None, text[i]))

    return nuevo_texto

    # stop_es = stopwords.words('spanish')
    # tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
    #                        encoding='latin-1', ngram_range=(1, 2), stop_words=stop_es)
    # features = tfidf.fit_transform(df.content).toarray()
    # labels = df.category_id
    # features.shape

# ahora devuelve el conteo de palabras por documento individualmente (quité el stopword porque juraria que en el stemmer ya lo hacemos)


def FreqTotalMatrix(text):
    # stop_es = stopwords.words('spanish')
    freq_matrix = [[]for y in range(GetNumberOfDocs(text))]
    for i in range(len(text)):
        freq_table = {}
        for word in text[i]:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        freq_matrix[i].append(freq_table)
        # print(str(freq_matrix))
    return(freq_matrix)

# numero de documentos en los que aparece la palabra


def FreqRelativeMatrix(text):
    # stop_es = stopwords.words('spanish')

    freq_table = {}
    for i in range(len(text)):
        aux_table = {}
        for word in text[i]:
            if word not in freq_table and word not in aux_table:
                freq_table[word] = 1
                aux_table[word] = 1
            elif word in freq_table and word not in aux_table:
                freq_table[word] += 1
                aux_table[word] = 1

    # print(freq_table)
    return(freq_table)


def CalculateTF(text, matrix):
    tf_list = [[]for y in range(GetNumberOfDocs(text))]
    for i in range(len(text)):
        totalNumber = len(text[i])
        word_n_tf = {}
        for j in range(len(matrix[i])):
            for word, count in (matrix[i][j]).items():
                print(word + "/ with count of " + str(count) +
                      " in total of " + str(totalNumber) + " words")
                # tf de cada palabra en su [][X] correspondiente
                tf = float(int(count)/totalNumber)
                word_n_tf[word] = tf
                # print("tf:" + str(tf))
                tf_list[i].append(word_n_tf)
    print(tf_list)
    return tf_list


def CalculateIDF(text, dictionary):
    word_n_idf = {}
    totalNumber = GetNumberOfDocs(text)

    for i in range(len(text)):
        for j in range(len(text[i])):
            for key in dictionary.keys():
                if str(text[i][j]) is key:
                    print(str(text[i][j]) + str(dictionary[key]))
                    idf = math.log(float(totalNumber / dictionary[key]))
                    word_n_idf[key] = idf

    print(word_n_idf)
    return word_n_idf


def tfIdf(tf_list, idf_list):

    tfidf_list = [[] for y in range(GetNumberOfDocs(tf_list))]
    for i in range(len(tf_list)):
        pass


# return total number of documents
def GetNumberOfDocs(text):
    number = 0
    for i in range(len(text)):
        number += 1

    return number


def getNumberofWords(text):
    cont = 0
    for i in range(len(text)):
        for word in text[i]:
            cont += 1
    return cont


class main():
    baseArray = lectura()
    numberOfDocs = GetNumberOfDocs(baseArray)
    # print(baseArray)
    tokenizedArray = tokenizado(baseArray)
    # print(tokenizedArray)
    lowerArray = LowerNTokenize(tokenizedArray)
    # print(lowerArray)
    stemmedString = Stemmer(lowerArray)
    # print(stemmedString)
    noemptyslotsString = NoEmpty(stemmedString)
    # print(noemptyslotsString)
    # matrixFreqString = FreqTotalMatrix(noemptyslotsString)
    # print(matrixFreqString)
    # tfList = CalculateTF(noemptyslotsString, matrixFreqString)

    freqRelMatrix = FreqRelativeMatrix(noemptyslotsString)
    # print(tfList)
    idfList = CalculateIDF(noemptyslotsString, freqRelMatrix)
    # tfIdf(tfList, idfList)

    # todo : cribar mierda DONE
    # todo : freq DONE
    # todo : tfidf
    # todo : similitud coseno
    # todo :  (select top 5 >> analisis de sentimientos)
