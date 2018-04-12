# Fake news detection


## Introduction

Within the expansion of social media and the internet, fake news has become an overwhelming
struggle to deal with. Since millions of people are exposed, the impact on public opinion is
significant.
Before going further, we should define literally a fake news:

- “False stories that seem to be news, spread on the internet or using other media, usually
    created to influence political views or as a joke” [1]
- “A made-up story with an intention to deceive” [7]

From that definition, we may think for an approach to identify them pragmatically in spite
of the variety, veracity and the amount of fake news data. The data shows up as aplain text
in a specific language which makes the process more difficult because every language has its
own semantics of word.


## I/O data

- Input data : The input data are news, we have gathered a tiny data set of 300 news for
    testing, on one hand we choose theHuffingtonpost[3] as an official source of news, On
    the other hand theRochdaleherald[5] as a source of sarcastic news.
- Output data : The output after the processing is a numerical score for each piece of news
    that will determine the category of it.



## Algorithmic analysis

### Description

As we go further, we noticed that the hypothesis was not correct, one of the problem that we
met, was the fact that some real news contain words that fall into the category of bad words as
a result the score increases overwhelmingly. For example, if the word”sex”appearsten times,
that does not necessarily mean that the piece of news is satire, so we decided to implement the
following process to deal with our problematic :

- For now, the algorithm used is a decision tree that has one value to evaluate for catego-
    rizing one piece of news.
- First and foremost, we had built our corpus of English news from two different sources,
    parsing their XML RSS feed we inserted them in a document oriented databaseMongodb
    hosted on a SaaSmLabunder the following schema:

 

```json
 {
  "title": "...",
  "summary" : "...",
  "source" : "Roch || Huff" }
```
- Filter all news by removing the words without meaning (i.e stop words) using Natural
    Language Toolkit.
- Determine a weight for each word using a text mining method namedTerm Frequency
    * Inverted Document Frequency[8], then sort them according to their weight in the
    document from the most to less relevant word.
- Verify, if the list of the 10 most relevant words contains a bad word, then increase its
    weight to make it even more relevant.
- Analyze the sentiment of each news title to obtain a subjectivity value that will be used
    to determine a score besides to thetfidfvalue of the previous step.
- At the end, by a generated score, evaluate if a news is satirical or undetermined.



### TF*IDF

TF*IDF, short term forTerm Frequency * Inverted Document Frequency, is a weighting
factor method used intext-miningto reflect the importance of words to a document in a
collection [8].
In fact it is an arithmetic product of two statics methods:

1. Term frequencytf(w, d) (1), is simply the occurrence frequency of a wordwin its own
    documentd. However the frequency is not enough to weight the relevance of a word,
    hence the idea of usingidf.

2. Inverted Document Frequency (2), is a log scaled value of the quotient that divides the
    size of a collectionNcby the number of documents in that collectiond∈cthat contains
    the word w, which represents the quantity of information that provides a word to its
    document, whether its common or rare through all documents of a collection.

3. Term Frequency * Inverted Document Frequency (3), is the product of the two functions
    mentioned above, as a result a word that occurs one time in two documents within a
    collection is more important and relevant than a word that occurs ten times in twenty
    documents of the same collection.

#### Sentiment Analysis

The information that could be extracted, with a sentiment analysis on a sentence, are:

1. The subjectivity expressed as a value in [0;1] (1 as 100% subjective)
2. The polarity expresses as numerical value in [-1;1] to show whether the sentence is negative
    or positive.

By using the sentiment analysis on a piece of news headline, we will determine both of
polarity and subjectivity(i.e: a common news headline are likely to be objective).
For the moment, the polarity is not significant enough to considerate it unlike the subjectivity
that is used to calculate the score (4).

#### Score

