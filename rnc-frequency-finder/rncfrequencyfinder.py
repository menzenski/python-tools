#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## rncfrequencyfinder.py Version 1.0 (2014-10-20)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: CC-BY-4.0 ( https://creativecommons.org/licenses/by/4.0/ )
##########

import urllib
import sgmllib
import lxml.html
import codecs

## designate a file with the words you want to search for
## (One word per line)
input_file = "listofwords_ignore.txt"

## designate a file for saving the results
## (this will be rewritten every time this script is run)
results_file = 'rncfrequencies_ignore.txt'

def corpus_search(search_term):
    '''Return the number of occurrences of a lemma (search_term) in the
       Russian National Corpus.'''

    # assemble a url including the search term
    search_url_begin = (
        "http://search.ruscorpora.ru/search.xml?mycorp="
        "&mysent=&mysize=&dpp=&spp=&spd=&text=lexgramm"
        "&mode=main&sort=gr_tagging&lang=en&parent1=0"
        "&level1=0&lex1="
        )
    
    search_url_end = (
        # "&gramm1=V%2Cipf&sem1=&flags1=&sem-mod1=sem&sem-mod1=sem2" # ipf verbs
        "&gramm1=&sem1=&flags1=&sem-mod1=sem&sem-mod1=sem2" # all words
        "&parent2=0&level2=0&min2=1&max2=1&lex2=&gramm2="
        "&sem2=&flags2=&sem-mod2=sem&sem-mod2=sem2"
        )
        
    search_url_whole = search_url_begin + search_term + search_url_end

    # load the page
    results_page = urllib.urlopen(search_url_whole)

    # read the results page html source
    results_html = results_page.read()
    
    # find the numbers in the results page html
    results_summary = lxml.html.find_class(results_html, "stat-number")
    # pull that text out
    result_numbers = [number.text for number in results_summary]
    # remove the spaces
    results_no_space = [number.replace(" ", "") for number in result_numbers]
    # convert that number from a (text) string to an integer
    result_integers = [int(number) for number in results_no_space]
    # make it printable in utf-8 encoding
    word = search_term.decode('utf8')

    # if there are any tokens of the search term, there will be several numbers
    # on the page. The fifth such number is the total tokens; that's the one
    # we want
    if len(result_integers) >= 5:
        word_results = result_integers[4]
    # if there are no results, there won't be any numbers, so we assign zero.
    else:
        word_results = 0
    return word_results

def main():
    with codecs.open(results_file, "a", encoding="utf-8") as stream:
        with open(input_file, 'r') as words:
            for line in words:
                for word in line.split():
                    freq = corpus_search(word)
                    stream.write("%s;%r\n" % (word.decode("utf-8"), freq))

if __name__ == '__main__':
    main()
