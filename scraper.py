from bs4 import BeautifulSoup
import requests
import csv
import numpy
import pandas as pd
import os
from django.conf import settings
import random
from fake_useragent import UserAgent
import time
import re

# getting user agent
ua = UserAgent()
#base URL
base_url="http://www.wsj.com/"
# URL that i want to scrape
url = "http://www.wsj.com/news/politics"
# start date
start_date = '2016-06-10'
# end date
end_date = '2016-10-21'

#my_date='2016-05-15'

#make random user agent
headers = {'User-Agent': str(ua.chrome)}
# dataframe where our data is saved
main_dataframe=pd.DataFrame()
set = True
while set == True:
    # getting main page
    html = requests.get(url,headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    # get all articles in the main page
    data_row = soup.find_all('div',{'class':'story-headline'})
    print("get all article")
    for x in range(0,len(data_row)):
        try:
            # get article url
            articleUrl = data_row[x].find('h3').a['href']
            html = requests.get(articleUrl,headers=headers ).text
            soup1 = BeautifulSoup(html, "lxml")
            article = soup1.body.findAll('article')
            # get article text
            text = ' '.join([s.text for s in article[0].findAll('p')])
            rx = re.compile('\W+')
            clean_text = rx.sub(' ', text).strip()
            raw_date = soup1.find('span',{'class':'pb-timestamp'})
            # get article date
            article_date=raw_date['content'].split('T')[0]
            # compare article data with our start date and end date
            if start_date < article_date <= end_date:
                print ("article in range, added to corpus: \n" + articleUrl)
                # make dataframe
                d = {'article_text' : [clean_text],'article_url':[articleUrl]}
                data_frame=pd.DataFrame(d)
                main_dataframe=main_dataframe.append(data_frame)
                time.sleep(random.randint(4,8))
            else:
                set=False
        except:
            print("video url " + articleUrl)

    loadmore = soup.find('div',{'class':'button pb-loadmore clear'})['data-contenturi']
    url=base_url+loadmore
# save article in csv
# set directory where you want to save the file and file name
main_dataframe.to_csv("/Volumes/companion/Google Drive/Fall 2016/NLP/project/article2.csv", sep=',',encoding='utf-8')
