#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import codecs
import urllib
import sgmllib
import lxml.html

def print_list(mylist):
    '''Print a list containing unicode characters.'''
    print '[' + ', '.join(
        "" + word.encode('utf8') + "" for word in mylist) + ']'

search_terms = [
    #'поити',
    'пошел', 'пошелъ', 'пошол', 'пошолъ',
    'пошла',
    'пошло',
    'пошли',
    'пошедше',
    'пошедъ',
    'поиде',
    'поидоша',
    #'ити',
    'шел', 'шелъ', 'шол', 'шолъ',
    'шла',
    'шло',
    'шли',
    'шедше',
    'шедъ',
    'иде',
    'идоша'
    ]

def get_source_date(source):
    """
    Return date for a source in the "Old Russian" subcorpus.

    If the given date for a source is a range, e.g., 1100-1150
    date_begin = 1100
    date_end = 1150
    date_middle = 1125
    """
    date_rough = source.split("(")
    date_long = date_rough[1][:-1]
    if len(date_long) > 1:
        dates = date_long.split("-")
        date_begin = int(dates[0])
        date_end = int(dates[1])
        date_middle = (date_begin + date_end) / 2
        return source
        return date_begin
        return date_end
        return date_middle
    elif len(date_long) == 1:
        date_begin = int(date_long)
        date_end = int(date_long)
        date_middle = int(date_long)
        return source
        return date_begin
        return date_end
        return date_middle
    else:
        pass
        
class RussianWord(object):
    """
    A word in the "old Russian" subcorpus of the Russian National Corpus.
    """

    def __init__(self, word):
        self.word = word
        self.word_printable = self.word.decode('utf8')
        self.total_frequency = 0
        self.sources = {}
        self.all_results_page_urls = []

    def general_corpus_search(self):
        """
        Conduct a search in "Old Russian" subcorpus and return number of hits.
        """
        search_url_begin = (
            "http://search.ruscorpora.ru/search.xml?env="
            "alpha&mode=mid_rus&text=lexform&sort=gr_created&lang="
            "ru&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp="
            "&spp=&spd=&req="
            )
        self.search_url_whole = search_url_begin + self.word

        self.results_page = urllib.urlopen(self.search_url_whole)
        self.results_html = self.results_page.read()
        self.bs = BeautifulSoup(self.results_html)
        self.results_summary = lxml.html.find_class(
            self.results_html, "stat-number")
        self.result_numbers = [number.text for number in self.results_summary]
        self.results_no_space = [number.replace(
            " ", "") for number in self.result_numbers]
        self.result_integers = [int(
            number) for number in self.results_no_space]

        if len(self.result_integers) >= 5:
            self.total_frequency = self.result_integers[4]
            return self.total_frequency
        else:
            self.total_frequency = 0
            return self.total_frequency

    def get_all_pages(self):
        ps = [p for p in self.bs.findAll('p', attrs={'class': 'pager'})]
        pager = ps[1]
        pages = [a for a in pager.findAll('a', href=True)]
        results_pages = pages[:-1]
        for pag in results_pages:
            self.all_results_page_urls.append(self.search_url_whole)
            self.all_results_page_urls.append(
                "http://search.ruscorpora.ru" + pag['href'])

    def get_sources_onepage(self):
        for span in self.bs.findAll('span', attrs={'class': 'b-doc-expl'}):
            a = span.find_next('a', href=True) # find <a> after <span>
            if a is not None:
                self.sources[span.string] = (
                    "http://search.ruscorpora.ru/" + a['href'])

    def get_tokens_onepage(self):
        for span in self.bs.findAll('span', attrs={'class': 'b-doc-expl'}):
            a = span.find_next('a', href=True) # find <a> after <span>
            if a is not None:
                self.sources[span.string] = (
                    "http://search.ruscorpora.ru/" + a['href'])

    def fetch_examples(self):
        self.sources = [item.string for item in pool.findAll(
            'span', attrs={'class': 'b-doc-expl'})]
        for source in sources:
            print source 

#    def find_bare_tokens(self):
#        for page in self.all_results_page_urls:

def main():
    #for search_term in search_terms:
        #search = Word(search_term)
        #search.fetch_examples()
    search = RussianWord("поиде")
    search.general_corpus_search()
    search.get_sources_onepage()
    #for key, value in search.sources.items():
    #    print key, value
    search.get_all_pages()
    for page in search.all_results_page_urls:
        print page
    
    #print search.sources
        

if __name__ == '__main__':
    main()
