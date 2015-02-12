#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## rncfrequencyfinder.py Version 1.0 (2014-10-20)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: CC-BY-4.0 ( https://creativecommons.org/licenses/by/4.0/ )
##########

import nltk, codecs
from unicodedata import category
from nltk.stem import SnowballStemmer

# text you'd like to stem
input_file = 'russiantext_ignore.txt'

# place to save the stemmed text
results_file = 'stemmedrussiantext_ignore.txt'

# list of all stemmed tokens
all_stems = []

punct = [u""".,;:'"`-„”()[]1234567890"""]

def get_stems(rus_text):
    unstemmed_text = codecs.open(rus_text, encoding="utf8").read()

    # strip punctuation marks
    unstemmed_text = ''.join(
        ch for ch in unstemmed_text if category(ch)[0] != 'P')
    
    tokens = nltk.word_tokenize(unstemmed_text)
    stemmer = SnowballStemmer("russian")

    for token in tokens:
        bare_stem = stemmer.stem(unicode(token))
        all_stems.append(bare_stem)
    

def main():
    get_stems(input_file)
    for stem in all_stems:
        print stem.encode('utf8'),

if __name__ == '__main__':
    main()
