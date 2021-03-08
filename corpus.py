import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem.snowball import SnowballStemmer

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
    
    testString = "Este es un texto de prueba para tokenizarlo"
    baseString = word_tokenize(testString,language="Spanish")
    baseString = LowerNTokenize(baseString)
    print(baseString)

    
    tokenizedString = Stemmer(baseString)


