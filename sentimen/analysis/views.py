from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.contrib import messages
from tablib import Dataset
import csv,io
import re
import numpy as np
import string
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, ArrayDictionary, StopWordRemover

from .models import *
from .forms import *

from django.http.response import JsonResponse

from django.core.serializers import serialize
import json

def home(request):

    return render(request, 'analysis/input_template.html')



def upload_tweet(request):
    tweets_to_delete = Tweet.objects.all()

    tweets_to_delete.delete()
    if request.method == 'POST':
        tweet_resource = TweetUploadForm()
        dataset = Dataset()
        new_tweet = request.FILES['myfile']

        data_set = new_tweet.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        idt1=1
        for column in csv.reader(io_string):
            created = Tweet.objects.update_or_create(
                    full_text=column[2],
                    username=column[10],
                    idt=idt1,
            )
            idt1+=1
    return render(request, 'analysis/input_template.html')

def list_tweet(request):
    items = Tweet.objects.all()
    
    data = {'items': json.loads(serialize('json', items))}
    return JsonResponse(data)

def delete_tweet(request, idt):
    tweets_to_delete = Tweet.objects.filter(idt=idt)

    tweets_to_delete.delete()

    return render(request, 'analysis/input_template.html')



#preprocessing data
nltk.download('stopwords')

stopwords_indonesia = stopwords.words('indonesian')

stop_factory = StopWordRemoverFactory().get_stop_words()
more_stopwords = [
    'yg', 'utk', 'cuman', 'deh', 'Btw', 'tapi', 'gua', 'gue', 'lo', 'lu',
    'kalo', 'trs', 'jd', 'nih', 'ntar', 'nya', 'lg', 'gk', 'ecusli', 'dpt',
    'dr', 'kpn', 'kok', 'kyk', 'donk', 'yah', 'u', 'ya', 'ga', 'km', 'eh',
    'sih', 'eh', 'bang', 'br', 'kyk', 'rp', 'jt', 'kan', 'gpp', 'sm', 'usah',
    'mas', 'sob', 'thx', 'ato', 'jg', 'gw', 'wkwk', 'mak', 'haha', 'iy', 'k',
    'tp', 'haha', 'dg', 'dri', 'duh', 'ye', 'wkwkwk', 'syg', 'btw',
    'nerjemahin', 'gaes', 'guys', 'moga', 'kmrn', 'nemu', 'yukkk',
    'wkwkw', 'klas', 'iw', 'ew', 'lho', 'sbnry', 'org', 'gtu', 'bwt',
    'klrga', 'clau', 'lbh', 'cpet', 'ku', 'wke', 'mba', 'mas', 'sdh', 'kmrn',
    'oi', 'spt', 'dlm', 'bs', 'krn', 'jgn', 'sapa', 'spt', 'sh', 'wakakaka',
    'sihhh', 'hehe', 'ih', 'dgn', 'la', 'kl', 'ttg', 'mana', 'kmna', 'kmn',
    'tdk', 'tuh', 'dah', 'kek', 'ko', 'pls', 'bbrp', 'pd', 'mah', 'dhhh',
    'kpd', 'tuh', 'kzl', 'byar', 'si', 'sii', 'cm', 'sy', 'hahahaha', 'weh',
    'dlu', 'tuhh'
]
data = stop_factory + more_stopwords

dictionary = ArrayDictionary(data)
str = StopWordRemover(dictionary)

factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])

# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])

# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)

def prepro(request):

    items = Tweet.objects.all()
    cleans_to_delete = Clean.objects.all()

    cleans_to_delete.delete()

    def remove_pattern(text, pattern_regex):
        r = re.findall(pattern_regex, text)
        for i in r:
            text = re.sub(i, '', text)
        return text

    cleaned_tweets = []

    for item in items:
        clean_tweet = remove_pattern(item.full_text, " *RT* | *@[\w]*")

        clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", clean_tweet).split())

        clean_tweet = re.sub(r'\$\w*', '', clean_tweet)
        clean_tweet = re.sub(r'^RT[\s]+', '', clean_tweet)
        clean_tweet = re.sub(r'#', '', clean_tweet)
        clean_tweet = re.sub('[0-9]+', '', clean_tweet)



        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
        tweet_tokens = tokenizer.tokenize(clean_tweet)

        tweets_clean = []
        for word in tweet_tokens:
            if (
                word not in stopwords_indonesia and  # remove stopwords
                word not in emoticons and  # remove emoticons
                word not in string.punctuation  # remove punctuation
            ):
                # Apply stemming
                stem_word = stemmer.stem(word)
                tweets_clean.append(stem_word)

        # Join the cleaned tokens back into a string
        tweets_clean  = " ".join([char for char in tweets_clean if char not in string.punctuation])
        cleaned_tweets.append((item.idt, tweets_clean, item.username))  


    # cleaned_tweets = list(set(cleaned_tweets))

    for idt, tweet, username in cleaned_tweets:
        Clean.objects.create(idt=idt, full_text=tweet, username=username)  

    cleaned_tweets = Clean.objects.all()
    return render(request, 'analysis/input_template.html')



