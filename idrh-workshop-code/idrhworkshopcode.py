#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## idrhworkshopcode.py Version 1.0 (2015-02-16)
##
## Code for the workshop "Introduction to Natural Language Processing
## with Python and the Natural Language Toolkit"
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: CC-BY-4.0 ( https://creativecommons.org/licenses/by/4.0/ )
##########

import nltk
import re
from urllib import urlopen

## get necessary data files, etc for the NLTK
nltk.download()

## ----------------------------------------------------------------------------
## Getting data from a plain-text file on the internet
##
# url = "http://menzenski.pythonanywhere.com/text/fathers_and_sons.txt"
# url = "http://www.gutenberg.org/cache/epub/30723/pg30723.txt" # alternative

## pythonanywhere made it harder to share files, so this is our workaround
url = "fathers_and_sons.txt"

## specify the path to your files
# pfx = "/home/<your pythonanywhere username>/<folder name>/"
pfx = "/home/menzenski/static/"

url = pfx + url

raw = urlopen(url).read()
## note that the above line is equivalent to the following two:
# webpage = urlopen(url)
# raw = webpage.read()

type(raw)
# <type "str">

len(raw)
# 448367

raw[:70]
# "The Project Gutenberg eBook, Fathers and Children, by Ivan Sergeevich\n"


## ----------------------------------------------------------------------------
## Tokenize the text

tokens = nltk.WordPunctTokenizer().tokenize(raw)

type(tokens)
# <type "list">

len(tokens)
# 91736

tokens[:10]
# ["The", "Project", "Gutenberg", "eBook", ",", "Fathers", "and", "Children",
# ",", "by"]

## ----------------------------------------------------------------------------
## More sophisticated text analysis with the NLTK

text = nltk.Text(tokens)

type(text)
# <class "nltk.text.Text">

text.collocations()
# Building collocations list
# Nikolai Petrovich; Pavel Petrovich; Anna Sergyevna; Vassily
# Ivanovitch; Madame Odintsov; Project Gutenberg-tm; Arina Vlasyevna;
# Project Gutenberg; Pavel Petrovitch.; Literary Archive; Gutenberg-tm
# electronic; Yevgeny Vassilyitch; Matvy Ilyitch; young men; Gutenberg
# Literary; every one; Archive Foundation; electronic works; old man;
# Father Alexey

raw.find("CHAPTER I")
# 1872

raw.rfind("***END OF THE PROJECT GUTENBERG")
# 429664

raw = raw[1872:429664]

raw.find("CHAPTER I")
# 0

## ----------------------------------------------------------------------------
## Pulling text from an HTML file
## web_url = "http://menzenski.pythonanywhere.com/text/blog_post.html"

## filename workaround, again
web_url = pfx + "blog_post.html"

web_html = urlopen(web_url).read()

web_html[:60]
# '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">\n<html><head>\n'

web_raw = nltk.clean_html(web_html)

web_tokens = nltk.word_tokenize(web_raw)

web_tokens[:10]
# ["This", "is", "a", "web", "page", "!", "This", "is", "a", "heading"]

web_tokens = web_tokens[10:410]

## ----------------------------------------------------------------------------
## Finding concordances
text.concordance("boy")
# Displaying 10 of 10 matches:
# ear ? Get things ready , my good boy : look sharp.' Piotr , who as a
#  of frogs , ' observed Vaska , a boy of seven , with a head as white
# t 's no earthly use. He 's not a boy , you know ; it 's time to throw
# y , drawing himself up. 'Unhappy boy ! ' wailed Pavel Petrovitch , he
# liberal. 'I advise you , my dear boy , to go and call on the Governor
# id in a low voice. 'Because , my boy , as far as my observations go ,
#  's seen ups and downs , my dear boy ; she 's known what it is to be
# der : 'You 're still a fool , my boy , I see. Sitnikovs are indispens
# ded , indicating a short-cropped boy , who had come in with him in a 
# tya. 'I am not now the conceited boy I was when I came here , ' Arkad

## ----------------------------------------------------------------------------
## Frequencies and stop words

fdist = nltk.FreqDist(text)

fdist
# <FreqDist with 10149 samples and 91376 outcomes>

vocab = fdist.keys()

vocab[:50]
# [",", "the", "to", "and", "a", "of", "'", "in", ";", "he", "you",
# "his", "I", "was", "?", "with", "'s", "that", "not", "her", "it",
# "at", "...", "for", "on", "!", "is", "had", "him", "Bazarov", "but",
# "as", "she", "--", "be", "have", "n't", "Arkady", "all",
# "Petrovitch", "are", "me", "do", "from", "up", "one", "I", "an",
# "my", "He", ]

# import re ## if you haven't already imported it (we did above in line 16)

# strip the punctuation
clean_text = ["".join(re.split("[.,;:!?`'-]", word)) for word in text]

fdist2 = nltk.FreqDist(clean_text)

vocab2 = fdist2.keys()

vocab2[:50]
# ["", "the", "to", "and", "a", "of", "in", "you", "I", "he", "his",
# "was", "with", "s", "that", "her", "not", "it", "at", "him",
# "Bazarov", "for", "on", "is", "had", "but", "as", "she", "Arkady",
# "Petrovitch", "be", "have", "me", "nt", "all", "are", "up", "do",
# "one", "from", "He", "my", "an", "The", "by", "You", "no", "your",
# "said", "what"]

# convert all words to lowercase (independent of stripping punctuation)
lower_text = [word.lower() for word in text]

fdist3 = nltk.FreqDist(lower_text)

vocab3 = fdist3.keys()

vocab3[:50]
# [",", "the", "to", "and", "a", "of", "'", "he", "in", "you", ";",
# "his", "i", "was", "?", "with", "that", "'s", "not", "her", "it",
# "at", "but", "she", "...", "for", "on", "is", "!", "had", "him",
# "bazarov", "as", "--", "be", "have", "n't", "arkady", "all",
# "petrovitch", "do", "are", "me", "one", "from", "what", "up", "my",
# "by", "an"]

# remove stop words

from nltk.corpus import stopwords

stopwords = stopwords.words("english")

content = [word for word in text if word.lower() not in stopwords]

fdist4 = nltk.FreqDist(content)

content_vocab = fdist4.keys()

content_vocab[:50]
# [",", "'", ";", "?", "'s", "...", "!", "Bazarov", "--", "n't", "Arkady", "Petrovitch", "one", "I", ".", "said", "Pavel", "like", "Nikolai", "little", "even", "man", "though", "know", "time", "went", "could", "say", "Anna", "would", "Sergyevna", "Vassily", "old", "What", "began", "'You", "come", "see", "Madame", "go", "Ivanovitch", "must", "us", "''", "eyes", "good", "young", "'m", "Odintsov", "without"]

# let's combine all three methods to clean up our distribution of words

text_nopunct = [''.join(re.split("[.,;:!?`'-]", word)) for word in text]

text_content = [word for word in text_nopunct if word.lower() not in stopwords]

fdist5 = nltk.FreqDist(text_content)

vocab5 = fdist5.keys()

vocab5[:50]
# ["", "Bazarov", "Arkady", "Petrovitch", "nt", "one", "said", "Pavel",
# "like", "Nikolai", "little", "man", "even", "time", "though", "know",
# "went", "say", "could", "Sergyevna", "Anna", "would", "Vassily",
# "began", "old", "see", "away", "us", "come", "eyes", "Ivanovitch",
# "good", "day", "face", "go", "Fenitchka", "Madame", "Yes", "Odintsov",
# "Katya", "must", "Well", "head", "father", "young", "Yevgeny", "long",
# "m", "back", "first"]

# we can also add to the list of stopwords:
more_stopwords = ["", "nt", "us", "m"] # et cetera
for stopword in stopwords:
    more_stopwords.append(stopword) # note: we're adding to "more_stopwords"

# remove updated stopwords list
text_content2 = [word for word in text_nopunct if word.lower(
    ) not in more_stopwords]

fdist6 = nltk.FreqDist(text_content2)

vocab6 = fdist6.keys()

vocab6[:50]
# ["Bazarov", "Arkady", "Petrovitch", "one", "said", "Pavel", "like",
# "Nikolai", "little", "man", "even", "time", "though", "know", "went",
# "say", "could", "Sergyevna", "Anna", "would", "Vassily", "began",
# "old", "see", "away", "come", "eyes", "Ivanovitch", "good", "day",
# "face", "go", "Fenitchka", "Madame", "Yes", "Odintsov", "Katya",
# "must", "Well", "head", "father", "young", "Yevgeny", "long", "back",
# "first", "think", "without", "made", "way"]

## ----------------------------------------------------------------------------
## frequency distributions and plots

type(fdist6)
# <class "nltk.probability.FreqDist"> # another custom nltk type

fdist6
# <FreqDist with 8118 samples and 38207 outcomes>

print fdist6
# <FreqDist: "Bazarov": 520, "Arkady": 391, "Petrovitch": 358, "one":
# 272, "said": 213, "Pavel": 197, "like": 192, "Nikolai": 182, "little":
# 164, "man": 162, ...>

# compare our first frequency distribution (before cleaning it up):
print fdist
# <FreqDist: ",": 6721, "the": 2892, "to": 2145, "and": 2047, "a": 1839,
# "of": 1766, "'": 1589, "in": 1333, ";": 1230, "he": 1155, ...>

fdist.plot(50, cumulative=True)

fdist6.plot(50, cumulative=True)

fdist.plot(50, cumulative=False)

fdist6.plot(50, cumulative=False)

## ----------------------------------------------------------------------------
## digging deeper into concordances

text6 = nltk.Text(text_content2)

text6.concordance("boy")
# Building index...
# Displaying 11 of 11 matches:
# Piotr hear Get things ready good boy look sharp Piotr modernised serv
# exquisite day today welcome dear boy Yes spring full loveliness Thoug
# unny afraid frogs observed Vaska boy seven head white flax bare feet
# while Explain please earthly use boy know time throw rubbish idea rom
# ount said Arkady drawing Unhappy boy wailed Pavel Petrovitch positive
# ugh reckoned liberal advise dear boy go call Governor said Arkady und
# reethinking women said low voice boy far observations go freethinkers
# arked Arkady seen ups downs dear boy known hard way charming observed
# ollowing rejoinder re still fool boy see Sitnikovs indispensable unde
# nt added indicating shortcropped boy come blue fullskirted coat ragge
#  owe change said Katya conceited boy came Arkady went ve reached twen

text.concordance("boy")
# Displaying 10 of 10 matches:
# ear ? Get things ready , my good boy : look sharp.' Piotr , who as a
#  of frogs , ' observed Vaska , a boy of seven , with a head as white
# t 's no earthly use. He 's not a boy , you know ; it 's time to throw
# y , drawing himself up. 'Unhappy boy ! ' wailed Pavel Petrovitch , he
# liberal. 'I advise you , my dear boy , to go and call on the Governor
# id in a low voice. 'Because , my boy , as far as my observations go ,
#  's seen ups and downs , my dear boy ; she 's known what it is to be
# der : 'You 're still a fool , my boy , I see. Sitnikovs are indispens
# ded , indicating a short-cropped boy , who had come in with him in a 
# tya. 'I am not now the conceited boy I was when I came here , ' Arkad

text.similar("boy")
# man child girl part rule sense sister woman advise and bird bit blade
# boast bookcase bottle box brain branch bucket

text.common_contexts(["boy", "girl"])
# a_of a_who # both of these words occurred between "a" and "of"
             # and between "a" and "who"

text.concordance("girl")
# Displaying 4 of 15 matches:
# stic housewife , but as a young girl with a slim figure , innocently
# o his two daughters -- Anna , a girl of twenty , and Katya , a child
#  paws , and after him entered a girl of eighteen , black-haired and
#  turned to a bare-legged little girl of thirteen in a bright red cot
