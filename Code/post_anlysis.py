#In this module we will build methods with which to
'''
Im going to assign 6 new columns ( Neu, Neg, Pos, bigramMatch%, unigramMatch%, perc_HashT_Match) Neu, neg and pos will give us the sentiment in the description, while bigramMatch% is the percentage of bigrams that match those produced by the fake news articles,  divided by the total number of bi-grams possible in the description. Unigram match will do the same thing but with all unigrams or single words that are found in the description.  Hashtag matches will follow similar logic, thus all three of these ranges [0,1]. We can use these attributes in our decision tree to split, hopefully, we see some strong matches, and then can confirm upon viewing the post that they are miss-info


'''
import nltk

import os
import string
import pandas as pd

 
import re 
import time 
import nltk.corpus  
import unidecode 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 
from autocorrect import Speller 
from bs4 import BeautifulSoup 
from nltk.corpus import stopwords 
from nltk import word_tokenize 
import string 


def gen_Sentiment( listt, dataframe ):
    '''
    This function takes in list of clean text and generates a score of neg, neu, or pos in the form of a dictionary.
    We then generate a new dataframe that will be return which include the description of the post cleaned, and the sentiment scores given by the nltk.sentiment SentimentIntensityAnalyzer
    
    '''
    
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer() 
    
    df2 = pd.DataFrame(columns = ['Desc','neg' , 'neu', 'pos'])
    
    for e in range(len(listt)):
        ee = str(dataframe['desc'][e])
        e1 = str(listt[e])
        score = sia.polarity_scores(ee)
        df2 = df2.append({'Desc': e1, 'neg':score['neg'], 'neu':score['neu'], 'pos':score['pos']}, ignore_index=True)
        
    df3 = pd.merge(dataframe, df2, left_index=True, right_index=True)
    return df3 

# def comp_bigram(text, listBigr):

def clean_single( desc ):
    '''
    input the raw description as a string
    
    Returned: Clean description 
    '''
    import re
    import func as fc2

    def rep(m):
        s=m.group(1)
        return ' '.join(re.split(r'(?=[A-Z])', s))

    text = re.sub(r'#(\w+)', rep, str(desc))
    text = fc2.remove_newLT(text)
    text = fc2.remove_Html(text)
    text = fc2.remove_white_numb(text)
    text = fc2.remove_doubles(text)
    text = fc2.expand_contrt(text)
    text = fc2.stopWords(text)
    return text



def ngrams1( sent, n):
    
    sent2 = clean_single( sent )
    
    token = [token for token in sent2.split(" ") if token != ""]
    ngrams = zip(*[token[i:] for i in range(n)])
    return [ ' '.join(ngrams) for ngrams in ngrams]


def gen_senti_onDesc( desc ):
    
    
    clean = clean_single( desc )
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer() 
    score = sia.polarity_scores(clean)
    
    return score

def gen_senti_onUncleanDesc( desc ):
    
    from nltk.sentiment import SentimentIntensityAnalyzer
    sia = SentimentIntensityAnalyzer() 
    score = sia.polarity_scores(desc)
    
    return score


def unigram_Score( desc ):
    
    
    #open the file containing all the unigrams and create a set out of it
    df = pd.read_csv("Data/unigram.csv")
    listUni = set(df['0'].tolist())
    
    
    #here we generate the possible unigrams for the description of the post
    list_Post_uni = set(ngrams1(desc, 1))
    
    interSect = set.intersection(listUni, list_Post_uni)
    set_sizeInter = len(interSect)
    set_sizeB = len(list_Post_uni)
    containment = set_sizeInter/set_sizeB
    
    return containment


def bigram_Score( desc ):
    
    
    #open the file containing all the unigrams and create a set out of it
    df = pd.read_csv("Data/bigram.csv")
    listbi = set(df['0'].tolist())
    
    
    #here we generate the possible unigrams for the description of the post
    list_Post_bi = set(ngrams1(desc, 2))
    
    
    interSect = set.intersection(listbi, list_Post_bi)
    set_sizeInter = len(interSect)
    set_sizeB = len(list_Post_bi)
    if set_sizeB <= 0:
        return 0
    else:
        containment = set_sizeInter/set_sizeB
    
    return containment


def combine_score( data ):
    
    inrange = data.index 
    
    df2 = pd.DataFrame(columns = ['Desc', 'Unigram_Score', 'Bigram_Score'])
    
    for e in range(len(data.index)):
        
        des = clean_single(str(data['Desc'][e]))
        uniS = unigram_Score(str(data['Desc'][e]))
        
        biS = bigram_Score(str(data['Desc'][e]))
        df2 = df2.append({'Desc':des, 'Unigram_Score': uniS, 'Bigram_Score': biS}, ignore_index=True)
        
                           
    
    data = data.drop('Desc', 1)
    merged = pd.merge(data, df2, left_index=True, right_index=True)
    return merged


def gen_sentimentBoth( data ):
    '''
    This function will take in a dataframe and allow you to generate two sentiment lists, the first list will contain the sentiment score defined by a clean text string. While the second list will contain the scores associated with uncleaned text
    
    '''
    liss = data['desc'].tolist()
    #here liss is the list of descriptions from the CSV
    cleaned = clean_single(liss[1])
    #looking to see the difference in sentiment score between cleaning and not
    #WE pass a single string cleaned into the analysis and we see that the cleaned text scores
    #make more sense then the scores produced by the analysis using an uncleaned string
    scrs1 = gen_senti_onDesc( cleaned)
    scrs2 = gen_senti_onUncleanDesc( liss[1])
    return (scrs1, scrs2)
                           