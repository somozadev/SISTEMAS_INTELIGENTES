from os import remove
import re
from nltk.corpus.reader import wordlist
import pandas as pd
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
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

#realiza el stemmer de los tweets tokenizados. también los pasa por una stoplist durante el stemmer
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
    nuevonuevo_texto[0].insert(0,'null')
    nuevonuevo_texto[1].insert(0,'null')
    nuevonuevo_texto.pop(0)
    nuevonuevo_texto.pop(0)

    return nuevonuevo_texto



# conteo de palabras por documento individualmente 
def FreqTotalMatrix(text):
    freq_matrix = [[]for y in range(GetNumberOfDocs(text))]
    for i in range(len(text)):
        freq_table = {}
        for word in text[i]:
            if word in freq_table:
                freq_table[word] += 1
            else:
                freq_table[word] = 1

        freq_matrix[i].append(freq_table)
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
    return(freq_table)


def CalculateTF(text, matrix):
    tf_list = [[]for y in range(GetNumberOfDocs(text))]
    for i in range(len(matrix)):
        totalNumber = len(matrix[i])
        word_n_tf = {}
        for j in range(len(matrix[i])):
            for word, count in (matrix[i][j]).items():
                # print(word + "/ with count of " + str(count) +" in total of " + str(totalNumber) + " words")
                tf = float(int(count)/totalNumber)
                word_n_tf[word] = tf
        tf_list[i].append(word_n_tf)
    return tf_list


def CalculateIDF(text, dictionary):
    word_n_idf = {}
    totalNumber = GetNumberOfDocs(text)
    for i in range(len(text)):
        for j in range(len(text[i])):
            for key in dictionary.keys():
                if str(text[i][j]) is key:
                    # print(str(text[i][j]) + str(dictionary[key]))
                    idf = math.log10(float(totalNumber / dictionary[key]))
                    word_n_idf[key] = idf
    return word_n_idf


def tfIdf(tf_list, idf_list):
    tfidf_list = [[] for y in range(GetNumberOfDocs(tf_list))]
    for i in range(len(tf_list)):
        for j in range(len(tf_list[i])):
            word_n_tfidf = {}
            for word, count in (tf_list[i][j]).items():
                for key in idf_list.keys():
                    if str(word) is key:
                        tfidfvalue = float(count*idf_list[key])
                        word_n_tfidf[key] = tfidfvalue
        tfidf_list[i].append(word_n_tfidf)
    return tfidf_list


def vectorizer(tfidf_list, dictionary):
    palabras = {}

    key_list = list(dictionary.keys())
    # print("keylist:" + str(key_list))
    # print("tfidf:" + str(tfidf_list))

    for i in range(len(key_list)):
        valor = [] 
        for tweet in range(len(tfidf_list)):
            
            # for elemento in range (len(tfidf_list[tweet])):
            #     print(str(tfidf_list[tweet]))
            # print(str(tfidf_list))
            # print((tfidf_list[tweet][0]).items())
            for word, count in (tfidf_list[tweet][0]).items():
                if(key_list[i] == word):
                    valor.append(count)
               
        print(len(valor))
        palabras[key_list[i]] = valor
    print(palabras)
# return total number of documents


def GetNumberOfDocs(text):
    number = 0
    for i in range(len(text)):
        number += 1
    return number


class main():
    
    
    baseArray = lectura()

    query = (str(input("Write query: ")))
    baseArray.append(query)

    numberOfDocs = GetNumberOfDocs(baseArray)
    # print(baseArray)
    tokenizedArray = tokenizado(baseArray)
    # print(tokenizedArray)
    lowerArray = LowerNTokenize(tokenizedArray)
    # print(lowerArray)
    stemmedString = Stemmer(lowerArray)
    # print(stemmedString)
    noemptyslotsString = NoEmpty(stemmedString)
    #print(noemptyslotsString)
    matrixFreqString = FreqTotalMatrix(noemptyslotsString)
    # print(matrixFreqString)
    tfList = CalculateTF(noemptyslotsString, matrixFreqString)
    #print(tfList)
    freqRelMatrix = FreqRelativeMatrix(noemptyslotsString)
    # print(freqRelMatrix)
    idfList = CalculateIDF(noemptyslotsString, freqRelMatrix)
    # print(idfList)
    tfidf_list = tfIdf(tfList, idfList)


    #* VALE TE CUENTO, HE PENSADO QUE PARA CALCULAR LA SIMILITUD DE COSENOS PODIAMOS AÑADIR LA QUERY
    #* AL FINAL DEL TODO, QUE SIGA LOS MISMOS PROCESOS Y QUE SE CALCULE COMO UN TWEET MÁS. LUEGO COGER
    #* ESA ULTIMA POSICION DEL TFIDF, CREAR OTRA TFIDF EXACTAMENTE IGUAL PERO VACÍO MENOS LA PARTE DE LA QUERY
    #* PARA CALCULAR CON ESOS DOS TDIDF´S EL COSENO Y LISTO. NO ESTÁ FUNCIONANDO COMO DEBERÍA Y CREO QUE SÉ 
    #* EL MOTIVO :https://treyhunner.com/2019/04/why-you-shouldnt-inherit-from-list-and-dict-in-python/
    #* BÁSICAMENTE, PYTHON Y LAS LISTAS Y DICCIONARIOS NO SE LLEVAN BIEN XD...
    #* estoy en un punto muerto y no se que cojonres hacer pa arreglar esto mas que rehacer todo todito todo y meterlo con
    #* alguna libreria o tutorial de porai.... que opinas ?



    query_tfidf_list = tfidf_list
    querySplit = noemptyslotsString[len(noemptyslotsString)-1]
    print("querySplit:"+str(querySplit))
    print("query trf start: " + str(query_tfidf_list))
    for i in range(len(query_tfidf_list)):  
        for j in range(len(query_tfidf_list[i])):
            for word, count in (query_tfidf_list[i][j]).items():
                for queryWord in querySplit:
                    # print("QueryWord: "+ str(queryWord) + "\n word: " + str(word) + "\n\n")
                    if  word != queryWord:
                        query_tfidf_list[i][j][word] = 0
                        
                    else:
                        query_tfidf_list[i][j][word] = count
                        print("\n ITS A MATCH \n")
                        print(" word: " + str(word)  + " count: " + str(count) )
                        print(str(list(query_tfidf_list[i][j].keys())[list(query_tfidf_list[i][j].values()).index(query_tfidf_list[i][j][word])]) + ": " + str(query_tfidf_list[i][j][word]))

                 
    for i in range(len(query_tfidf_list)):  
        for j in range(len(query_tfidf_list[i])):
            print("query trf end: " + str(query_tfidf_list[i][j].items()))
    # vectorizer(tfidf_list, freqRelMatrix)
    print("LenTF" + str(len(tfList)))
    print("LenIDF" + str(len(idfList)))
    print("LenTF-IDF" + str(len(tfidf_list)))

    # todo : cribar mierda DONE
    # todo : freq DONE
    # todo : tfidf DONE
    # todo : similitud coseno
    # todo :  (select top 5 >> analisis de sentimientos)
