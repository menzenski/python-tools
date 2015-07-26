#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## rnchistoricalsearcher.py Version 0.1 (2015-07-23)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: MIT ( http://opensource.org/licenses/MIT )
##
##
### The MIT License (MIT)
###
### Copyright (c) 2015 Matt Menzenski
###
### Permission is hereby granted, free of charge, to any person obtaining a
### copy of this software and associated documentation files (the "Software"),
### to deal in the Software without restriction, including without limitation
### the rights to use, copy, modify, merge, publish, distribute, sublicense,
### and/or sell copies of the Software, and to permit persons to whom the
### Software is furnished to do so, subject to the following conditions:
###
### The above copyright notice and this permission notice shall be included in
### all copies or substantial portions of the Software.
###
### THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
### OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
### FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
### THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
### LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
### FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
### DEALINGS IN THE SOFTWARE.
##
##########

"""Return frequency and year for items in the historical corpora of the RNC."""

from urllib import FancyURLopener
from bs4 import BeautifulSoup as Soup
import re
import urlparse

## from: http://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-python-urlopen
#def url_encode_non_ascii(b):
#    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)
#
#def iri_to_url(iri):
#    parts = urlparse.urlparse(iri)
#    return urlparse.urlunparse(
#        part.encode('idna') if parti==1 else url_encode_non_ascii(
#            part.encode('utf-8'))
#        for parti, part in enumerate(parts)
#    )

class RNCSource(object):
    """One source in RNC search results."""

    def __init__(self, source_name_as_string):

        self.source = source_name_as_string
        self.date_string = ''
        self.date_begin = 0   # earliest date given
        self.date_middle = 0  # middle of date range
        self.date_end = 0     # latest date given
        self.name = re.sub(r'\([^)]*\)', '', self.source)

    def dates(self):
        """Return source dates as numeric values (float or int)."""

        if re.findall('\(.*?\)', self.source):
            self.date_string = re.findall('\(.*?\)', self.source)

            ## DATES OF TYPE (1400-1500), (1441-1442)
            if re.findall('\A\d{4}-\d{4}\Z', self.date_string[0][1:-1]):
                dates = re.findall('\A\d{4}-\d{4}\Z', self.date_string[0][1:-1])
                self.date_begin = int(dates[0].split("-")[0])
                self.date_end = int(dates[0].split("-")[1])
                self.date_middle = (self.date_begin + self.date_end) / 2.0

            ## DATES OF TYPE (1550), (1570)
            elif len(self.date_string) == 6:
                date_year = int(re.findall(
                    '\A\d{4}\Z', self.date_string[0][1:-1])[0])
                self.date_begin = date_year
                self.date_middle = date_year
                self.date_end = date_year

            ## DATES OF TYPE (1423.02.20), (1436.06.13)
            elif len(self.date_string) == 12:
                date_year = int(re.findall(
                    '\A\d{4}', self.date_string[0][1:-1])[0])
                self.date_begin = date_year
                self.date_middle = date_year
                self.date_end = date_year

            ## TODO: Is this elif clause captured by the next one? (Yes?)
            ## Date given inside parentheses but in some other format
            elif re.findall('\d{4}', self.date_string[0])[0]:
                date_year = int(re.findall('\d{4}', self.date_string[0])[0])
                self.date_begin = date_year
                self.date_middle = date_year
                self.date_end = date_year

        ## if date is given outside parentheses (less common)
        elif re.findall('\d{4}', self.source):
            date_year = int(re.findall('\d{4}', self.source))
            self.date_begin = date_year
            self.date_middle = date_year
            self.date_end = date_year

        ## TODO: decide if this else statement can just be scrapped altogether
        else:
            print "No date found"


class MyOpener(FancyURLopener):
    """FancyURLopener object with custom User-Agent field."""

    ## regular Mac Safari browser:
    #version = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
    #           "AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 "
    #           "Safari/600.5.17")

    ## identify this web scraper as such
    ## and link to a page with a description of its purpose:
    version = ("Web scraper created by Matt Menzenski. "
               "See www.menzenski.com/scraper for more information.")


class Webpage(object):
    """Generic webpage with attributes."""

    def __init__(self, address):
        self.address = address
        myopener = MyOpener()
        self.html = myopener.open(self.address).read()
        self.soup = Soup(self.html)
        #try:
        #    self.html = myopener.open(self.address).read()
        #    self.soup = Soup(self.html)
        #except UnicodeError:
        #    self.html = myopener.open(iri_to_url(self.address)).read()
        #    self.soup = Soup(self.html)


class RNCSearchTerm(object):
    """Object containing all (past-tense) forms of a search term."""
    ## this really just provides a namespace for organizing search terms.

    def __init__(self):
        # ancient corpus needs lemmas and grammatical forms
        self.ancient_forms = ['iperf', 'aor', 'perf', 'past']
        self.ancient_splx_ipf = []
        self.ancient_pfx_pf = []
        self.ancient_pfx_ipf = []

        # old corpus needs individual word forms, not lemmas
        self.old_splx_ipf = []
        self.old_pfx_pf = []
        self.old_pfx_ipf = []

        # modern corpus needs lemmas and grammatical forms
        self.modern_forms = ['praet']
        self.modern_splx_ipf = []
        self.old_pfx_pf = []
        self.old_pfx_ipf = []

class RNCWord(object):
    """One word in RNC search results (any subcorpus), with grammatical information."""

    def __init__(self, span):
        """Initialize RNCWord object."""

        pass

class RNCWordExplainAncient(object):
    """Pop-up explanation page for a word in the ancient RNC subcorpus."""

    def __init__(self, mode="old_rus", sort="gr_created", lang="ru",
                 doc="", parent1=0, level1=0, lexi1="", gramm1="",
                 parent2=0, level2=0, min2=1, max2=1, text="word-info",
                 requestid=1437941630686, language="ru", source=""):
        """Initialize with empty search parameters."""

        self.mode = mode
        self.sort = sort
        self.lang = lang
        self.doc = doc
        self.parent1 = parent1
        self.level1 = level1
        self.lexi1 = lexi1
        self.gramm1 = gramm1
        self.parent2 = parent2
        self.level2 = level2
        self.min2 = min2
        self.max2 = max2
        self.text = text
        self.requestid = requestid
        self.language = language
        self.source = source

        self.params = {
            "mode": self.mode,
            "sort": self.sort,
            "lang": self.lang,
            "doc": self.doc,
            "parent1": self.parent1,
            "level1": self.level1,
            "lexi1": self.lexi1,
            "gramm1": self.gramm1,
            "parent2": self.parent2,
            "level2": self.level2,
            "min2": self.min2,
            "max2": self.max2,
            "text": self.text,
            "requestid": self.requestid,
            "language": self.language,
            "source": self.source,
            }

    def explain_url_ancient(self):
        """Generate explaination url from parameters."""

        self.address = u"http://search-beta.ruscorpora.ru/search-explain.xml?"

        for k, v in self.params.iteritems():
            self.address += u"{}={}&".format(k, v)

        return self.address

    def scrape_explain_ancient(self):
        """Get grammatical and semantic info for a word in ancient subcorpus."""

        self.explain_url_ancient()

        page = Webpage(self.address)

        self.surface_form = page.soup.find('span', attrs={"class": "cs"}).string
        self.lemma = self.surface_form.find_next('td', attrs={"class": "value"}).string

        self.surface_form = unicode(self.surface_form)
        self.lemma = unicode(self.lemma)



class RNCSearchAncient(object):
    """Search of the 'ancient' subcorpus of the Russian National Corpus."""

    def __init__(self, mode="old_rus", text1="lexgramm",
                 sort="gr_created", lang="ru",
                 doc_docid="0|13|2|3|1|4|7|8|10|12|5|11|9|6",
                 parent1=0, level1=0, lexi1="", gramm1="",
                 parent2=0, level2=0, min2=1, max2=1):
        """Initialize with empty search parameters."""

        self.mode = mode
        self.text1 = text1
        self.doc_docid = doc_docid
        self.parent1 = parent1
        self.level1 = level1
        self.lexi1 = lexi1
        self.gramm1 = gramm1
        self.parent2 = parent2
        self.level2 = level2
        self.min2 = min2
        self.max2 = max2

        self.params = {
            "mode": self.mode,
            "text": self.text1,
            "doc_docid": self.doc_docid,
            "parent1": self.parent1,
            "level1": self.level1,
            "lexi1": self.lexi1,
            "gramm1": self.gramm1,
            "parent2": self.parent2,
            "level2": self.level2,
            "min2": self.min2,
            "max2": self.max2,
            }

        self.results_page_urls = []

    def base_search_url(self):
        """Generate a search url from parameters."""

        self.address = "http://search-beta.ruscorpora.ru/search.xml?"

        for k, v in self.params.iteritems():
            self.address += "{}={}&".format(k, v)

        return self.address

    def addresses_ancient(self):
        """Return list of results page urls from a search of 'ancient' RNC."""

        page_idx = 0
        self.base_search_url()
        self.address = self.address + "p={}&".format(page_idx)
        while 1:
            ## TODO: change this line so it doesn't keep adding the same thing
            #new_string = re.sub(r'"(\d+),(\d+)"', r'\1.\2', original_string)
            self.address = re.sub(r'p=(\d+?)&', 'p={}&'.format(
                page_idx), self.address)

            #self.address += "p={}&".format(page_idx)
            page = Webpage(self.address)

            try:
                if page.soup.ol.findAll('li'):
                    page_idx += 1
                    self.results_page_urls.append(self.address)
                    #print "Hey! {}\n\n".format(self.address)
            except AttributeError:
                break
            else:
                break

    def scrape_one_page_ancient(self, url):
        """Return source, date, and token for one page of results from 'ancient' RNC."""

        page = Webpage(url)
        sources_on_page = []
        for itm in page.soup.ol.findAll('li'):
            sources = itm.find_all('span', attrs={'class': 'b-doc-expl'})
            for source in sources:
                src = RNCSource(source.string)
                print src.name

                source_list = source.find_next('ul')
                words = source_list.find_all('span', attrs={'class': 'b-wrd-expl g-em cs'})
                for word in words:
                    #print u"{};{}".format(word.string, word.get('explain'))
                    #
                    #expl = RNCWordExplainAncient(
                    #    lexi1=word.string, source=word.get('explain')
                    #    )
                    #
                    #expl.explain_url_ancient()
                    #print "{}\n\n".format(expl.address)
                    print self.lexi1
                    print self.gramm1
                    print word.string



class RNCSearchOld(object):
    """Search of the 'old' subcorpus of the Russian National Corpus."""

    def __init__(self):
        pass

#    def base_search_url(self):
#        """Generate a search url from parameters."""
#
#        self.address = "http://search-beta.ruscorpora.ru/search.xml?"
#
#        for k, v in self.params.iteritems():
#            self.address += "{}={}&".format(k, v)
#
#        return self.address

    def base_search_url():
        pass

    def addresses_old(self):
        """Return list of results page urls from a search of 'old' RNC."""

        page_idx = 0
        self.base_search_url()
        self.address = self.address + "p={}&".format(page_idx)
        while 1:
            ## TODO: change this line so it doesn't keep adding the same thing
            #new_string = re.sub(r'"(\d+),(\d+)"', r'\1.\2', original_string)
            self.address = re.sub(r'p=(\d+?)&', 'p={}&'.format(
                page_idx), self.address)

            #self.address += "p={}&".format(page_idx)
            page = Webpage(self.address)

            try:
                if page.soup.ol.findAll('li'):
                    page_idx += 1
                    self.results_page_urls.append(self.address)
                    #print "Hey! {}\n\n".format(self.address)
            except AttributeError:
                break
            else:
                break

    def scrape_one_page_old(self, url):
        """Return source, date, and token for one page of results from 'old' RNC."""

        pass


class RNCSearchModern(object):
    """Search of the 'modern' corpus of the Russian National Corpus."""

    def __init__(self, mycorp="", mysent="", mysize="",
                 dpp="", spp="", spd="", text="lexgramm",
                 mode="main", sort="gr_tagging", lang="en",
                 parent1=0, level1=0, lex1="", gramm1="",
                 sem1="", flags1="", sem_mod1="",
                 sem_mod2="", parent2=0, level2=0, min2=1,
                 max2=1, lex2="", gramm2="", sem2="",
                 flags2=""):
        """Initialize with empty search parameters."""

        self.mycorp = mycorp
        self.mysent = mysent
        self.mysize = mysize
        self.dpp = dpp
        self.spp = spp
        self.spd = spd
        self.text = text
        self.mode = mode
        self.sort = sort
        self.lang = lang
        self.parent1 = parent1
        self.level1 = level1
        self.lex1 = lex1
        self.gramm1 = gramm1
        self.sem1 = sem1
        self.flags1 = flags1
        self.sem_mod1 = sem_mod1
        self.sem_mod2 = sem_mod2
        self.parent2 = parent2
        self.level2 = level2
        self.min2 = min2
        self.max2 = max2
        self.lex2 = lex2
        self.gramm2 = gramm2
        self.sem2 = sem2
        self.flags2 = flags2

        # fetch number of resulting tokens
        self.search_results = 0

        # parameters for search URL generation
        self.params = {
            "mycorp": self.mycorp,
            "mysent": self.mysent,
            "mysize": self.mysize,
            "dpp": self.dpp,
            "spp": self.spp,
            "spd": self.spd,
            "text": self.text,
            "mode": self.mode,
            "sort": self.sort,
            "lang": self.lang,
            "parent1": self.parent1,
            "level1": self.level1,
            "lex1": self.lex1,
            "gramm1": self.gramm1,
            "sem1": self.sem1,
            "flags1": self.flags1,
            "sem-mod1": self.sem_mod1,
            # "sem-mod1": ,
            "parent2": self.parent2,
            "level2": self.level2,
            "min2": self.min2,
            "max2": self.max2,
            "lex2": self.lex2,
            "gramm2": self.gramm2,
            "sem2": self.sem2,
            "flags2": self.flags2,
            "sem-mod2": self.sem_mod2
            #"sem-mod2": ,
            }

    def base_search_url(self):
        """Generate a search url from parameters."""

        self.address = "http://search.ruscorpora.ru/search.xml?"

        for k, v in self.params.iteritems():
            self.address += "{}={}&".format(k, v)

        return self.address

    def addresses_modern(self):
        """Return list of results page urls from a search of 'modern' RNC."""

        page_idx = 0
        self.base_search_url()
        self.address = self.address + "p={}&".format(page_idx)
        while 1:
            ## TODO: change this line so it doesn't keep adding the same thing
            #new_string = re.sub(r'"(\d+),(\d+)"', r'\1.\2', original_string)
            self.address = re.sub(r'p=(\d+?)&', 'p={}&'.format(
                page_idx), self.address)

            #self.address += "p={}&".format(page_idx)
            page = Webpage(self.address)

            try:
                if page.soup.ol.findAll('li'):
                    page_idx += 1
                    self.results_page_urls.append(self.address)
                    #print "Hey! {}\n\n".format(self.address)
            except AttributeError:
                break
            else:
                break

    def scrape_one_page_modern(self, url):
        """Return source, date, and token for one page of results from 'modern' RNC."""

        pass


def main():
    ubrati = RNCSearchTerm()
    # lemmas for the ancient subcorpus
    ubrati.ancient_splx_ipf = ["брати", "бьрати"]
    ubrati.ancient_pfx_pf = ["убрати", "убьрати"]
    ubrati.ancient_pfx_ipf = ["убирати"]
    # word forms for the old subcorpus
    ubrati.old_splx_ipf = [""]
    ubrati.old_pfx_pf = [""]
    ubrati.old_pfx_ipf = [""]
    # lemmas for the modern subcorpus
    ubrati.modern_splx_ipf = ["брать"]
    ubrati.modern_pfx_pf = ["убрать"]
    ubrati.modern_pfx_ipf = ["убирать"]

    sobrati = RNCSearchTerm()
    # lemmas for the ancient subcorpus
    sobrati.ancient_splx_ipf = ["брати", "бьрати"]
    sobrati.ancient_pfx_pf = ["събрати", "събьрати", "собрати", "собьрати"]
    sobrati.ancient_pfx_ipf = ["събирати", "собирати"]
    # word forms for the old subcorpus
    sobrati.old_splx_ipf = [""]
    sobrati.old_pfx_pf = [""]
    sobrati.old_pfx_ipf = [""]
    # lemmas for the modern subcorpus
    sobrati.modern_splx_ipf = ["брать"]
    sobrati.modern_pfx_pf = ["собрать"]
    sobrati.modern_pfx_ipf = ["собирать"]

    for lemma in sobrati.ancient_splx_ipf:
        for form in sobrati.ancient_forms:
            search = RNCSearchAncient(lexi1=lemma,gramm1=form)
            search.base_search_url()
            search.addresses_ancient()

            for url in search.results_page_urls:
                print "{}\n\n".format(url)
                search.scrape_one_page_ancient(url)

    for lemma in sobrati.ancient_pfx_pf:
        for form in sobrati.ancient_forms:
            search = RNCSearchAncient(lexi1=lemma,gramm1=form)
            search.base_search_url()
            search.addresses_ancient()

            for url in search.results_page_urls:
                print "{}\n\n".format(url)
                search.scrape_one_page_ancient(url)

    for lemma in sobrati.ancient_pfx_ipf:
        for form in sobrati.ancient_forms:
            search = RNCSearchAncient(lexi1=lemma,gramm1=form)
            search.base_search_url()
            search.addresses_ancient()

            for url in search.results_page_urls:
                print "{}\n\n".format(url)
                search.scrape_one_page_ancient(url)

#    for lemma in ubrati.modern_splx_ipf:
#        for form in ubrati.modern_forms:
#            print "{},{}".format(lemma, form)
#            search = RNCSearchModern(lex1=lemma,gramm1=form)
#            search.base_search_url()
#            print search.address


if __name__ == "__main__":
    main()
