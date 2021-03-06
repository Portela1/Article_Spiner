import random
import nltk
import numpy as np
from bs4 import BeautifulSoup



positive_rive = BeautifulSoup(open('positive.review').read(),features="html.parser")
positive_rive = positive_rive.findAll('review_text')

negative_rive = BeautifulSoup(open('negative.review').read(),features="html.parser")
negative_rive = negative_rive.findAll('review_text')

trigrams = {}

for review in positive_rive:
    word = review.text.lower()
    tokens = nltk.tokenize.word_tokenize(word)
    for i in range(len(tokens)-2):
        k = (tokens[i],tokens[i+2])
        if k not in trigrams:
            trigrams[k] = []
        trigrams[k].append(tokens[i+1])

trigram_probabilities = {}

for k,words in trigrams.items():
    if len(set(words)) > 1:
        d={}
        n = 0
        for w in words:
            if w not in d:
                d[w] = 0
            d[w] +=1
            n +=1
        for w,c in d.items():
            d[w] = float(c) / n
        trigram_probabilities[k] = d


def random_sample(d):
    r = random.random()
    cumulative = 0
    for w,p in d.items():
        cumulative += p
        if r<cumulative:
            return w

def test_spinner():
    review = random.choice(positive_rive)
    s = review.text.lower()
    print("Original: ",s)
    tokens = nltk.tokenize.word_tokenize(s)
    for i in range(len(tokens) - 2):
        if random.random() < 0.2:
            k = (tokens[i],tokens[i+2])
            if k in trigram_probabilities:
                w = random_sample(trigram_probabilities[k])
                tokens[i+1] = w
    print("Spun: ")
    print(" ".join(tokens))



test_spinner()