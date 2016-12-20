#! python
import sys
from sys import argv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import os
import csv

script, in_file, out_file = argv
SIA = SentimentIntensityAnalyzer()

shortword = re.compile(r'\W*\b\w{25,100000}\b')

def articleToSentiment(file):
    article = shortword.sub('', file)
    sentiments = SIA.polarity_scores(article)
    return sentiments

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

with open(out_file, 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    with open(in_file, 'rb') as mycsvfile:
        thedata = csv.reader(mycsvfile, dialect='mydialect')
        row = next(thedata)
        row.append('P.Score')
        row.append('N.Score')

        for row in thedata:
            article_text = row[2]
            article_date = row[3]
            article_sentiment = articleToSentiment(article_text)
            thedatawriter.writerow([article_date, article_sentiment['pos'],
                                    article_sentiment['neg']])



            print("Article Date: %s \n \n P.Score: %s \t\t N.Score: %s \n %s"
            % (article_date, article_sentiment['pos'], article_sentiment['neg'],
            '-------------------- -------------------- --------------------'))
