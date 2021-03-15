import pandas as pd
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
# textplob? >> replace
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

#limpia los espacios en blanco 
def NoEmpty(text):
    nuevo_texto = [[]]
    for i in range(len(text)):
        for j in range(len(text[i])):
            text[i][j] = re.sub("[^A-Za-z0-9]", '', text[i][j])
        
        nuevo_texto.append(text[i])    # text[i][j] = re.findall( ' ', text[i][j])
 

    for i in range(len(text)):        
        nuevo_texto[i] = list(filter(None, text[i]))

    return nuevo_texto

    # stop_es = stopwords.words('spanish')
    # tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
    #                        encoding='latin-1', ngram_range=(1, 2), stop_words=stop_es)
    # features = tfidf.fit_transform(df.content).toarray()
    # labels = df.category_id
    # features.shape

def FreqMatrix(text):
    stop_es = stopwords.words('spanish')
    freq_matrix = [[]for y in range(GetNumberOfDocs(text))]
    for i in range(len(text)):
        for word in text[i]:
            freq_table = {}
            for stopword in stop_es:
                if word in stopword:
                    continue
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1
            freq_matrix[i].append(freq_table)
            
    print(freq_matrix)        
            # print("fmatrix" + freq_matrix)

#return total number of documents
def GetNumberOfDocs(text):
    number = 0
    for i in range(len(text)):
        number += 1
    
    return number

def getNumberofWords(text):
    cont=0
    for i in range(len(text)):
        for word in text[i]:
            cont +=1
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
    FreqMatrix(noemptyslotsString)

    # todo : cribar mierda, y pesos tfidf + similitud coseno (select top 5 >> analisis de sentimientos)
