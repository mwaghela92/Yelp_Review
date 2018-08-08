# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:51:21 2018

@author: mayur
"""

import pandas as pd

train_df = pd.read_csv('E:/mayur/Yelp_Review/Data/yelp.csv')

train_df.head(5)
text = train_df['text']

from SPARQLWrapper import SPARQLWrapper, JSON
import requests
import urllib.parse
from nltk.corpus import stopwords

from retry import *

BASE_URL = 'http://api.dbpedia-spotlight.org/en/annotate?text={text}&confidence={confidence}&support={support}'
#Text = 'Obama born 1961 Honolulu, Hawaii, two years after territory admitted Union 50th state. Raised largely Hawaii, he also spent one year his childhood Washington. four years Indonesia. After graduating Columbia Universty 1983, he worked community organizer Chicago.He loved Paris. The france national team won the worldcup 2018 and that was amazing. he travelled by jet airways'
CONFIDENCE = '0.5'
SUPPORT = '500'

#Text = Text.split()
#Text1 = [word for word in Text if word not in stopwords.words('english')]
#TEXT = ' '.join(Text1)
entities = pd.DataFrame({'person' : [0],'place': [0],'animal': [0],
                                       'city': [0], 'country': [0],
                                       'organisation': [0],'Food': [0]})
   

for i in range(1):
    TEXT = text[1]
    REQUEST = BASE_URL.format(
        text=urllib.parse.quote_plus(TEXT), 
        confidence=CONFIDENCE, 
        support=SUPPORT
    )
    HEADERS = {'Accept': 'application/json'}
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    all_urls = []
    
    r = retried_func(url = REQUEST , headers=HEADERS)
    response = r.json()
    
    resources = response['Resources']
    
    for res in resources:
        all_urls.append(res['@URI'])
    
    x = list()
    
    for i in range(len(all_urls)):
        #i=0
        
        values = '(<{0}>)'.format(all_urls[i])
        
        
       # values = '(<{0}>)'.format('>) (<'.join(all_urls))
    
        sparql.setQuery(
        """PREFIX vrank:<http://purl.org/voc/vrank#>
           SELECT DISTINCT ?l
           FROM <http://dbpedia.org> 
           FROM <http://people.aifb.kit.edu/ath/#DBpedia_PageRank>
           WHERE {
               VALUES (?s) {""" + values + 
        """    }
           ?s rdf:type ?p .
           ?p rdfs:label ?l.
           FILTER (lang(?l) = 'en')
        } limit 6
            """)
    
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        x.append([])
        for result in results["results"]["bindings"]:
            x[i].append( result['l']['value'])
        
        
    item = list()
    for res in resources:
        item.append(res['@surfaceForm'])
    
    mainlist = {}
    j = 0
    for i in item:
        mainlist[i] = x[j]
        j = j +1
    
    for i in mainlist:
        print(i,':', mainlist[i][:])
        print ('\n')
        
   
    #entities = pd.DataFrame(columns = ['ProperNoun','person','place','animal',
     #                                  'city', 'country','organisation','Food'])
    #entities.ProperNoun = item
    
    
    for i in mainlist:   
        print(i)
        for j in range(1,len(entities.columns)):
            if (entities.columns[j] in mainlist[i][:]):
                    entities.loc[0,entities.columns[j]]= entities.loc[0,entities.columns[j]] + 1  
        
                    
    
   
        