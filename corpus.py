import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


#En este bloque se crea la matriz TF-IDF con los stopwords de español
stop_es=stopwords.words('spanish')
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words=stop_es)
features = tfidf.fit_transform(df.content).toarray()
labels = df.category_id
features.shape


def lectura():
    values=[]
    df = pd.read_excel('tweets.xlsx', sheet_name='Search Twitter')
    for i in df.index:
        values.append(df['Text'][i])
    return values

def tokenizado(testStringArray):
    arrayTokenizado=[]
    for i in testStringArray:
        aux = word_tokenize(i, language="Spanish")
        arrayTokenizado.append(aux)
        print(aux)
    return arrayTokenizado



def LowerNTokenize(baseString):
    i = 0
    newBaseString = baseString
    for word in baseString:
        word = word.lower()
        newBaseString[i] = word 
        i = i+1
    return newBaseString

def Stemmer(tokenized_text):
    stemmer = SnowballStemmer('spanish')
    stemmed_txt = [stemmer.stem(i) for i in tokenized_text]
    print(stemmed_txt)
    return stemmed_txt

class main():
    baseArray=lectura()
    arrayTokenizado= tokenizado(baseArray)
    #baseString = LowerNTokenize(baseString)
    #print(baseString)

    
    #tokenizedString = Stemmer(baseString)


