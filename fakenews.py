import feedparser
import math
import re   
from pymongo import MongoClient
import html
import nltk
import json
from nltk.corpus import stopwords # Import the stop word list
from textblob import TextBlob as tb


def connecToDatabse():
    client = MongoClient('mongodb://ecam_algo:ecamalgo2018@ds012168.mlab.com:12168/fakenews')
    return client
    

def setNews(client):
    db = client.fakenews
    collection = db.news
    d = feedparser.parse("http://www.huffingtonpost.co.uk/feeds/index.xml")
    re2 = '<.*?>'
    for e in d.entries:
        news = {"title" : e.title, 
                "summary" : html.unescape(re.sub(re2, '', e.summary.replace("\n",""))), 
                "source" : "Huff"}
        collection.insert_one(news)
        

def setFakeNews(client):
    db = client.fakenews
    collection = db.news
    d = feedparser.parse("https://rochdaleherald.co.uk/feed/")
    re2 = '<.*?>'
    for e in d.entries:
        news = {"title" : e.title, 
                "summary": html.unescape(re.sub(re2, '', e.content[0].value)), 
                "source" : "Roch"}
        collection.insert_one(news)


'''def getAllNews(collection):
    
    cursor = collection.find({})
    for document in cursor:'''


def getMeaningfulWords(client):
    db = client.fakenews
    collection = db.news
    stops = stopwords.words("english")
    cursor = collection.find({})
    result = dict()
    for document in cursor:
        meaningfulWords = re.sub("[^a-zA-Z]"," ", document["summary"])
        meaningfulWords = meaningfulWords.lower().split()
        meaningfulWords = [w for w in meaningfulWords if not w in stops]
        #result[str(document["_id"])] = " ".join( meaningfulWords )
        result[str(document["_id"])] = meaningfulWords 
    return result

def getBadWords():
    badwords = json.load(open('badwords.json'))
    return badwords["badwords"]

def detectBadWords(meaningfulWords, badwords):
   # print(meaningfulWords['5aa108e3b3f7112e30054ecd'])
    for k, v in meaningfulWords.items():
        numberOfMeaningfulWords = len(v)
        numberOfBadWords = len([w for w in v if w in badwords])

def getMostImportantWords(meaningfulWords):
    for k, v in meaningfulWords.items():
        #print("Top words in document {}".format(k))
        result = tb(" ".join(v))
        scores = {word: tfidf(word, result, meaningfulWords) for word in result.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if (k == '5aa108e3b3f7112e30054ecd'): 
            for word, score in sorted_words[:10]:
                print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))

def tf(word, meaningfulWordsValue):
    return meaningfulWordsValue.words.count(word) / len(meaningfulWordsValue)

def n_containing(word, meaningfulWords):
    return sum(1 for v in meaningfulWords if word in v) 

def idf(word, meaningfulWords):
    return math.log(len(meaningfulWords) / (1 + n_containing(word, meaningfulWords)))

def tfidf(word, meaningfulWordsValue, meaningfulWords):
    return tf(word, meaningfulWordsValue) * idf(word, meaningfulWords)

        

# ObjectId('5aa108e2b3f7112e30054eb5')


if __name__ == '__main__':
    client = connecToDatabse()
    result = getMeaningfulWords(client)
    badWords = getBadWords()
    detectBadWords(result, badWords)
    getMostImportantWords(result)

