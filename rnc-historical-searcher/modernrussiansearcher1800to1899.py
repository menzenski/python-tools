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

lemmas = [
    'пойти',
    'идти'
    ]

forms = [
    'praet'
    ]
        
class RussianWord(object):

    def __init__(self, lemma, form):
        self.word = lemma
        self.form = form
        self.word_printable = self.word.decode('utf8')
        self.total_frequency = 0
        self.sources = {}
        self.all_results_page_urls = []

    def general_corpus_search(self):
        search_url_begin = (
            "http://search.ruscorpora.ru/search.xml?env="
            "alpha&mycorp=%28%28created%253A%253E%253D%25221800"
            "%2522%29%2520%2526%2526%2520%28created"
            "%253A%253C%253D%25221899%2522%29%29&mysent=&mysize="
            "48985844&mysentsize=3617178&mydocsize=3486&spd=&text="
            "lexgramm&mode=main&sort=gr_tagging&lang=ru&nodia="
            "1&parent1=0&level1=0&lex1="
            )

        search_url_middle = "&gramm1="

        search_url_end = (
            "&sem1=&sem-mod1=sem&sem-mod1=sem2&flags1="
            "&m1=&parent2=0&level2=0&min2=1&max2=1&lex2="
            "&gramm2=&sem2=&sem-mod2=sem&sem-mod2=sem2&flags2=&m2="
            )
        
        self.search_url_whole = (
            search_url_begin + self.word + search_url_middle +
            self.form + search_url_end
            )

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
        self.all_results_page_urls.append(self.search_url_whole)
        for pag in results_pages:
            self.all_results_page_urls.append(
                "http://search.ruscorpora.ru" + pag['href'])

    def no_really_get_all_pages(self):
        tenth_results_page = urllib.urlopen(self.all_results_page_urls[9])
        tenth_results_html = tenth_results_page.read()
        page_soup = BeautifulSoup(tenth_results_html)
        ps = [p for p in page_soup.findAll('p', attrs={'class': 'pager'})]
        pager = ps[1]
        pages = [a for a in pager.findAll('a', href=True)]
        results_pages = pages[:-1]
        for page in results_pages:
            if page not in self.all_results_page_urls:
                self.all_results_page_urls.append(
                    "http://search.ruscorpora.ru" +page['href'])

    def seriously_get_all_pages(self):
        page_nums = [
            '0','1','2','3','4','5','6','7','8',
            '9','10','11','12','13','14','15'
            ]
        suffix = "&p="
        all_page_urls = []
        for page_num in page_nums:
            new_page_url = self.search_url_whole + suffix + page_num
            all_page_urls.append(new_page_url)
        self.all_results_page_urls = all_page_urls
#        for page_url in self.all_results_pages: # just checking
#            print page_url

    def i_am_not_kidding(self):
        page_nums = range(0,178)
        suffix = "&p="
        all_page_urls = []
        for page_num in page_nums:
            new_page_url = self.search_url_whole + suffix + str(page_num)
            all_page_urls.append(new_page_url)
        self.all_results_page_urls = all_page_urls
#        for page_url in self.all_results_pages: # just checking
#            print page_url

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

    def find_bare_tokens(self):
        for page in self.all_results_page_urls:
            results_page_one = urllib.urlopen(page)
            results_html_one = results_page_one.read()
            bs1 = BeautifulSoup(results_html_one)
            
            sources = [item for item in bs1.findAll(
                'span', attrs={'class': 'b-doc-expl'})]
            
            for span in bs1.findAll('span', attrs={'class': 'b-doc-expl'}):
                a = span.find_next('a', href=True) # find <a> after <span>
                source_name_full = span.string
                if "(" in source_name_full:
                    source_name_split = source_name_full.rsplit("(", 1)
                    source_name = source_name_split[0]
                    source_name_1 = source_name_split[1].split(")")
                    source_date_long = source_name_1[0]
                
                    if "-" in source_date_long:
                        date_split = source_date_long.split("-")
                        date_begin = int(date_split[0])
                        date_end = int(date_split[1])
                        date_mid = (date_begin + date_end) / 2.0
                    elif ("." in source_date_long
                          and "-" not in source_date_long): 
                        source_date_2 = source_date_long.split(".")
                        source_date_3 = source_date_2[0]
                        date_begin = int(source_date_3)
                        date_end = int(source_date_3)
                        date_mid = int(source_date_3)
                    elif ("." not in source_date_long and
                          "-" not in source_date_long):
			if source_date_long.isalnum():
                            date_begin = int(source_date_long)
                            date_end = int(source_date_long)
                            date_mid = int(source_date_long)
			else:
			    date_begin = 0
			    date_end = 0
			    date_mid = 0
                    else:
                        date_begin = "whoops!"
                else:
                    source_name = source_name_full
                    source_date_long = 'NoDateGiven'
                    date_begin = 0
                    date_mid = 0
                    date_end = 0
                
                    
                if a is not None:
                    source_url = ("http://search.ruscorpora.ru/" + a['href'])
                    source_link_text_list = a.contents
                    source_link_text_1 = "".join(source_link_text_list)
                    source_link_text_2 = source_link_text_1.split("\n")
                    source_link_text = source_link_text_2[0]
                    source_hits_1 = source_link_text.split("(")
                    source_hits_2 = source_hits_1[1].split(")")
                    source_hits_3 = source_hits_2[0]
                    source_hits_4 = source_hits_3.encode('ascii', 'ignore')
                    source_hits = int(source_hits_4)
#                    print "%r\n%s\n%s (from %r to %r to %r), %s\n%s\n%s" % (
#                        source_hits,
#                        source_name_full,
#                        source_date_long, date_begin, date_mid, date_end,
#                        source_name,
#                        source_link_text,
#                        self.word.decode('utf8')
#                        )
                    for i in range(source_hits):
#                        print "%s;%r;%s;%s;%r;%r;%r;%s" % (
#                            source_link_text, source_hits,
#                            self.word.decode('utf8'),
#                            source_date_long, date_begin, date_mid, date_end,
#                            source_name
#                            )
                        print "%s;%s;%r;;%s;%r;%r;%r;%s;%s" % (
                            self.form,
                            source_link_text, source_hits,
                            self.word.decode('utf8'),
                            source_date_long, date_begin, date_mid, date_end,
                            source_name,
                            )
            

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
#    for page in search.all_results_page_urls:
#        print page
    search.find_bare_tokens()
    
    #print search.sources

def main_two():
    for search_term in search_terms:
        search = RussianWord(search_term)
        search.general_corpus_search()
        search.get_sources_onepage()
        search.get_all_pages()
        search.find_bare_tokens()

def main_three():
    for lemma in lemmas:
        for form in forms:
            search = RussianWord(lemma, form)
            search.general_corpus_search()
            search.get_sources_onepage()
            search.get_all_pages()
            search.no_really_get_all_pages()
            search.find_bare_tokens()

def main_four():
    for lemma in lemmas:
        for form in forms:
            search = RussianWord(lemma, form)
            search.general_corpus_search()
            search.get_sources_onepage()
            search.i_am_not_kidding()
            search.find_bare_tokens()

if __name__ == '__main__':
    main_four()
