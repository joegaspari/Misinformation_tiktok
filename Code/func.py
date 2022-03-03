''' 
The purpose of func.py is to store all working methods used int preProc.ipynb

All functions will be defined using a doc string

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

import matplotlib.pyplot as plt

import spacy


def load_ext():
    '''
    Load_ext: This function will take open the fakenews.csv file and extract a list of article titles as text data which will be cleaned using the following methods in this func.py file.
    
    Returns: list of text strings 
    '''
    
    df = pd.read_csv("Data/fakeNews.csv")
    list1 = df['Text'].tolist()
    
    return list1


def remove_newLT(text):
    '''
    This input takes in a line of text data from the data frame or list and removes all new line or tab characters.
    
    This input will also correct spaces found in . com links
    
    '''
    
    reform = ( text.replace('\\n', ' ')
              .replace('\n', ' ')
              .replace('\t',' ')
              .replace('\\', ' ')
              .replace('. com', '.com') )
    
    return reform

def remove_Html(text):
    '''
    This method takes in text data and removes all links and .com 
    '''
    
    basket = BeautifulSoup(text, "html.parser")
    strippedT = basket.get_text(separator=" ")
    
    #here we are removing all http presence using regex re.sub to capture our link fragments
    remove_https = re.sub(r'http\S+', '', strippedT)
    remove_com = re.sub(r"\ [A-Za-z]*\.com", " ", remove_https)
    
    return remove_com

def remove_white_numb(text):
    '''
    Remove_white takes in text data, in the form of a string and removes all additional white space found in the text.
    
    Returns: Cleaned text without extra whitespaces
    
    '''
    pattern = re.compile(r'\s+') 
    
    Without_whitespace = re.sub(pattern, ' ', text)
    
    text = Without_whitespace.replace('?', ' ? ').replace(')', ') ')
    
    text = re.sub(r'\d+', '', text)
    
    text = re.sub(r'[^\w\s]', '', text)
    
    return text



def remove_doubles(text):
    '''
    Remove_doubles: Will correct any duplicate characters that may have accidentally been added via the user when entering the data.
    
    Returns: Text without duplicate characters
    
    
    '''
    #first we begin by converting all elements of the text to lower case
    text = text.lower()
    
    # Pattern matching for all case alphabets
    Pattern_alpha = re.compile(r"([A-Za-z])\1{1,}", re.DOTALL)
    
    # Limiting all the  repeatation to two characters.
    Formatted_text = Pattern_alpha.sub(r"\1\1", text) 
    
    # Pattern matching for all the punctuations that can occur
    Pattern_Punct = re.compile(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}')
    
    # Limiting punctuations in previously formatted string to only one.
    Combined_Formatted = Pattern_Punct.sub(r'\1', Formatted_text)
    
    # The below statement is replacing repeatation of spaces that occur more than two times with that of one occurrence.
    Final_Formatted = re.sub(' {2,}',' ', Combined_Formatted)
    
    return Final_Formatted



def expand_contrt(text):
    '''
    
    expand_contrt: Will intake a string element and begins to search word for word, for contractions to expand wihtin the text data. This function also removes all special characters that do not belong or contribute to the significance of the words we are looking for. Also accented or unique characters that are not unicode are effectively removed or revereted to their unicode equivielent
    
    Returns: Text data with expanded contractions 
    
    '''
    
    #The english language holds a massive number of contractions, the full list of contractions can be found on wikipedia list of contractions (https://en.wikipedia.org/wiki/Wikipedia:List_of_English_contractions)
    contractions = {"ain't": "is not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so as",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have",
    }
    
    
    #we begin by tokeninzing the text
    word_tokens = text.split(' ')

    
    for w in word_tokens:
        if w in contractions:
            #replace contracted word
            word_tokens = [item.replace(w, contractions[w]) for item in word_tokens]
            
    
    reform = ' '.join(str(w) for w in word_tokens)
    
    #removing all special characters as well
    reform = re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', reform) 
    
    #This segment confirms that all characters represented in the text segment are unicode
    reform2 = unidecode.unidecode(reform)
    return reform2


def remove_nonE(text):
    '''
    If a word is found to be slang, or not found within the normal corpus of words used in the english language then the word will be stripped from the text data
    
    *Not sure how effective this is once the words have neen spell checked
    
    Returns: text that has been stripped of non-english words
    '''
    word_tokens = text.split(' ')
    wordz = set(nltk.corpus.words.words())
    
    reform = ""
    for w in word_tokens:
        if w in wordz:
            reform += w+" "
        else:
            reform += ""
            
    return reform
    
    
    
def spellck(text):
    '''
    spellck: Takes in a string of text data and checks each word using the python spellchecker
    
    
    Returns: correctly spelt words
    '''
    
    spell = Speller(lang='en')
    cor = spell(text)
    
    return cor


def stopWords(text):
    '''
    here we will build an extensive list of stop words that are used in the english language that do not provide additional significance to what the fragment's meaning is. 
    
    '''
    
    Stop_nltk = list(stopwords.words('english'))
    
    en = spacy.load('en_core_web_sm')
    Stop_spacy = list(en.Defaults.stop_words)
    
    stopW = Stop_nltk + Stop_spacy
    
    #Now Stop_nltk and Stop_spacy contain a list of (179 + 326) 505 words
    
    words = [word for word in text.split() if word not in stopW]
    # words now contains all words that were not found in the list of 505
    newT = " ".join(words)
    
    return newT

def clean( listt ):
    '''
    Clean will iterate over each list element and then perform text cleaning on this element, the function will return a complete 
    list cleaned 
    
    '''
    #Create an empty list to add our cleaned text to in the same order which they occur in the orginial list
    cleaned = []
    
    for e in listt:
        text = remove_newLT(e)
        text = remove_Html(text)
        text = remove_white_numb(text)
        text = remove_doubles(text)
        text = expand_contrt(text)
        text = stopWords(text)
        cleaned.append(text)
        

        
    return cleaned


def creat_corpus( lst ):
    doc = ""
    for e in lst:
        doc = doc+" "+e
    
    return doc

