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
from nltk.stem import SnowballStemmer

# text you'd like to stem
input_file = 'russiantext.txt'

# place to save the stemmed text
results_file = 'stemmedrussiantext.txt'

# list of all stemmed tokens
all_stems = []

def get_stems(rus_text):
    unstemmed_text = codecs.open(rus_text, encoding="utf8").read()
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
