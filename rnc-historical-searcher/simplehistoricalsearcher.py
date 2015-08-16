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
from openpyxl import Workbook
import re
import time
import random

class ResultsSpreadsheet(Workbook):
    """Excel spreadsheet containing search results."""

    def __init__(self, filename):
        super(ResultsSpreadsheet, self).__init__()
        self.filename = filename
        self.active.title = "Results"

    def write_row(self, row_idx, dict_contents):
        """Write dict to row number row_idx in the ResultsSpreadsheet.

        row_idx: an integer representing a row number.
        dict_contents: a dictionary in which the keys are column numbers
        and the values are the corresponding contents, e.g., {1: 'Modern'}.
        """

        for k, v in dict_contents.iteritems():
            c = self.active.cell(row=row_idx, column=k)
            c.value = v

    def save_wb(self):
        """Save the ResultsSpreadsheet to file."""

        self.save("{}.xlsx".format(self.filename))

    def write_headers(self):
        """Add headers in first row of spreadsheet."""

        header_dict = {
            1: u"Subcorpus",
            2: u"BaseVerb",
            3: u"Lemma",
            4: u"PrefixValue",
            5: u"Prefix",
            6: u"SuffixValue",
            7: u"Suffix",
            8: u"SourceName",
            9: u"SourceDateBegin",
            10: u"SourceDateMiddle",
            11: u"SourceDateEnd",
            12: u"NumberOfTokens"
            }

        self.write_row(row_idx=1, dict_contents=header_dict)


class RNCSource(object):
    """One source in RNC search results."""

    def __init__(self, source_name_as_string):
        self.source = source_name_as_string
        self.date_begin = 0   # earliest date given
        self.date_middle = 0  # middle of date range
        self.date_end = 0     # latest date given
        self.name = re.sub(r'\([^)]*\)', '', self.source)

    def dates(self):
        """Return source dates as numeric values (float or int)."""

        dates = re.findall(r'\d{4}', self.source)
        if len(dates) == 2:
            self.date_begin = float(dates[0])
            self.date_end = float(dates[1])
            self.date_middle = (self.date_begin + self.date_end) / 2.0

        elif len(dates) == 1:
            self.date_begin = float(dates[0])
            self.date_middle = float(dates[0])
            self.date_end = float(dates[0])

        else:
            pass

class MyOpener(FancyURLopener):
    """FancyURLopener object with custom User-Agent field."""

    ## regular Mac Safari browser:
    version = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
        "AppleWebKit/600.5.17 (KHTML, like Gecko) Version/8.0.5 "
        "Safari/600.5.17"
        )

    ## identify this web scraper as such
    ## and link to a page with a description of its purpose:
    #version = ("Web scraper created by Matt Menzenski. "
    #           "See www.menzenski.com/scraper for more information.")

class Webpage(object):
    """Generic webpage with attributes."""

    def __init__(self, address):
        self.address = address
        myopener = MyOpener()
        delay = random.randint(0,4)
        time.sleep(delay)
        self.html = myopener.open(self.address).read()
        self.soup = Soup(self.html)
        #try:
        #    self.html = myopener.open(self.address).read()
        #    self.soup = Soup(self.html)
        #except UnicodeError:
        #    self.html = myopener.open(iri_to_url(self.address)).read()
        #    self.soup = Soup(self.html)

class RussianVerb(object):
    """Russian verb object: provides namespace for possible forms."""

    def __init__(self, simplex_verb):

        self.root = simplex_verb
        self.prefixed_forms = {}

        self.prefixes = {
            # path/location prefixes
            'o-': ['о', 'об', 'обо', 'объ'],
            'nad-': ['над', 'надо', 'надъ'],
            'pere-': ['пере', 'пре', 'прѣ'],
            'pro-': ['про'],
            'u-': ['у'],
            'na-': ['на'],
            # goal prefixes
            'v-': ['в', 'во', 'въ'],
            'pri-': ['при'],
            'za-': ['за'],
            'do-': ['до'],
            's-': ['с', 'со', 'съ'],
            # source prefixes
            'iz-': ['из', 'изо', 'изъ'],
            'vy-': ['вы'],
            'ot-': ['от', 'ото', 'отъ'],
            'voz-': ['вз', 'вс', 'воз', 'вос', 'взо', 'взъ', 'возъ'],
            'raz-': ['раз', 'рас', 'разо', 'разъ'],
            # po
            'po': ['по'],
            }

        self.prefixes_with_null = self.prefixes
        self.prefixes_with_null['—'] = ['']

        self.prefixed_forms = []
        for k, v in self.prefixes.iteritems():
            for pfx in v:
                self.prefixed_forms.append("{}{}".format(pfx, self.root))

        self.prefixed_forms_by_prefix = {}
        for k, v in self.prefixes.iteritems():
            forms = [pfx + self.root for pfx in v]
            self.prefixed_forms_by_prefix[k] = forms

        self.all_forms_by_prefix = self.prefixed_forms_by_prefix
        self.all_forms_by_prefix['—'] = ['' + self.root]


class RNCSearchTerm(object):
    """Container object holding all (past-tense) forms of a search term."""
    ## we're really just providing a convenient namespace for handling terms.

    def __init__(self):
        ## the ancient corpus needs both lemmas and grammatical categories
        self.ancient_forms = ['iperf', 'aor', 'perf', 'past']
        self.ancient_splx_ipf = [] # simplex imperfective lemmas
        self.ancient_pfx_pf = []   # prefixed perfective lemmas
        self.ancient_pfx_ipf = []  # prefixed imperfective lemmas

        ## the old corpus needs individual word forms only, NOT lemmas
        self.old_splx_ipf = []     # simplex imperfective word forms
        self.old_pfx_pf = []       # prefixed perfective word forms
        self.old_pfx_ipf = []      # prefixed imperfective word forms

        ## the modern corpus needs both lemmas and grammatical categories
        self.modern_forms = ['praet']
        self.modern_splx_ipf = []  # simplex imperfective lemmas
        self.modern_pfx_pf = []    # prefixed perfective lemmas
        self.modern_pfx_ipf = []   # prefixed imperfective lemmas

class RNCQueryAncient(object):
    """Object describing a query of the Ancient RNC subcorpus."""

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

        self.base_url = "http://search-beta.ruscorpora.ru/search.xml?"

class RNCQueryOld(object):
    """Object describing a query of the Old RNC subcorpus."""

    def __init__(self, env="alpha", mode="mid_rus", text="lexform",
            sort="gr_created", lang="ru", mycorp="", mysent="",
            mysize="", mysentsize="", mydocsize="", dpp="",
            spp="", spd="", req=""):
        """Initialize with empty search parameters."""

        self.env = env
        self.mode = mode
        self.text = text
        self.sort = sort
        self.lang = lang
        self.mycorp = mycorp
        self.mysent = mysent
        self.mysize = mysize
        self.mysentsize = mysentsize
        self.mydocsize = mydocsize
        self.dpp = dpp
        self.spp = spp
        self.spd = spd
        self.req = req

        self.params = {
            "env": self.env,
            "mode": self.mode,
            "text": self.text,
            "sort": self.sort,
            "lang": self.lang,
            "mycorp": self.mycorp,
            "mysent": self.mysent,
            "mysize": self.mysize,
            "mysentsize": self.mysentsize,
            "mydocsize": self.mydocsize,
            "dpp": self.dpp,
            "spp": self.spp,
            "spd": self.spd,
            "req": self.req,
            }

        self.base_url = "http://search-beta.ruscorpora.ru/search.xml?"

class RNCQueryModern(object):
    """Object describing a query of the Modern RNC subcorpus."""

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

        self.base_url = "http://search.ruscorpora.ru/search.xml?"

class RNCSearch(object):
    """A search of one of the three historical RNC subcorpora."""

    def __init__(self, rnc_query, subcorpus="", pfx_val="",
            sfx_val="", lem="", base_verb="", prefix="", suffix=""):
        """Initialize search object.

        Parameters
        ----------
          rnc_query:  RNCQueryAncient(), RNCQueryOld(), or RNCQueryModern()
          subcorpus:  'Ancient', 'Old', or 'Modern'
          pfx_val:    'yesPrefix' or 'noPrefix'
          sfx_val:    'yesSuffix' or 'noSuffix'
          lem:        e.g., 'собирать'
          base_verb:  e.g., 'брать'
          prefix:     e.g., 'ot-'
          suffix:     e.g., '-yva-'

        """

        self.subcorpus = subcorpus
        self.pfx_val = pfx_val
        self.sfx_val = sfx_val
        self.lem = lem
        self.base_verb = base_verb
        self.prefix = prefix
        self.suffix = suffix

        self.params = rnc_query.params
        self.address = rnc_query.base_url
        self.results_page_urls = []

        ## list of dicts
        self.all_search_results = []

    def base_search_url(self):
        """Generate a search url from parameters."""
        for k, v in self.params.iteritems():
            self.address += "{}={}&".format(k, v)

        return self.address

#    def addresses(self):
#        """Return a list of all pages of results from an RNC search."""
#
#        page_idx = self.p
#        self.base_search_url()
#
#        still_results = True
#        while still_results:
#
#            address = self.address + "p={}&".format(page_idx)
#            page = Webpage(address)
#
#            a = page.soup.ol.find_all('li')
#            if a is not None:
#                self.results_page_urls.append(address)
#                page_idx += 1
#            elif a is None:
#                still_results = False
#
#            #try:
#            #    if page.soup.ol.findAll('li'):
#            #        self.results_page_urls.append(address)
#            #        page_idx += 1
#            #    elif not page.soup.ol.findAll('li'):
#            #        still_results = False
#            #except AttributeError as e:
#            #    print "AttributeError: {}\n{}".format(e, address)
#            #    still_results = False
#            #except Exception as e:
#            #    print "Exception!"
#            #    print e.__str__
#            #    print e.message
#            else:
#                print "Some other error in self.addresses():\n{}".format(
#                    address)
#                still_results = False

#    def scrape_results_pages(self):
#        """Return frequency and year information from results pages."""
#
#        for address in self.results_page_urls:
#            page = Webpage(address)
#            soup = page.soup
#
#            #sources = [src for src in soup.ol.find_all(
#            #    'li') if src.contents[4].string.startswith(u"Все")]
#
#            sources_on_page = []
#
#            lis = soup.ol.find_all('li')
#            for li in lis:
#                if li.contents[4].string.startswith(u"Все"):
#                    sources_on_page.append(li)
#                elif li.contents[4].string.startswith(u"All"):
#                    sources_on_page.append(li)
#                else:
#                    pass
#
#            for source in sources_on_page:
#                source_name = source.contents[0].string
#                src_obj = RNCSource(source_name)
#                src_obj.dates()
#                examples = re.search(ur'(\d+)', source.contents[4].string)
#                if examples:
#                    source_examples = int(examples.group(0))
#                else:
#                    source_examples = 0
#
#                print "\nAddress: {}".format(address)
#                print u"\nName: {}\nDate(s): {},{},{}\nExamples: {}\n".format(
#                    source_name, src_obj.date_begin, src_obj.date_middle,
#                    src_obj.date_end, source_examples
#                    )
#
#                row_dict = {
#                    1: "{}".format(self.subcorpus),
#                    2: "{}".format(self.base_verb),
#                    3: "{}".format(self.lem),
#                    4: "{}".format(self.pfx_val),
#                    5: "{}".format(self.prefix),
#                    6: "{}".format(self.sfx_val),
#                    7: "{}".format(self.suffix),
#                    8: u"{}".format(source_name),
#                    9: src_obj.date_begin,
#                    10: src_obj.date_middle,
#                    11: src_obj.date_end,
#                    12: source_examples
#                    }
#
#                self.all_search_results.append(row_dict)

    def scrape_one_page(self, soup):
        """Scrape the content of one page.

        Parameters
        ----------
        soup: BeautifulSoup() object of a webpage
        """

        sources_on_page = []

        lis = soup.ol.find_all('li')
        for li in lis:
            if li.contents[4].string.startswith(u"Все"):
                sources_on_page.append(li)
            elif li.contents[4].string.startswith(u"All"):
                sources_on_page.append(li)
            else:
                pass

        for source in sources_on_page:
            source_name = source.contents[0].string
            src_obj = RNCSource(source_name)
            src_obj.dates()
            examples = re.search(ur'(\d+)', source.contents[4].string)
            if examples:
                source_examples = int(examples.group(0))
            else:
                source_examples = 0

            row_dict = {
                1: "{}".format(self.subcorpus),
                2: "{}".format(self.base_verb),
                3: "{}".format(self.lem),
                4: "{}".format(self.pfx_val),
                5: "{}".format(self.prefix),
                6: "{}".format(self.sfx_val),
                7: "{}".format(self.suffix),
                8: u"{}".format(source_name),
                9: src_obj.date_begin,
                10: src_obj.date_middle,
                11: src_obj.date_end,
                12: source_examples
                }
            self.all_search_results.append(row_dict)


    def scrape_pages(self):
        """More straightforward scraping method."""

        self.base_search_url()
        page_idx = 0

        has_more_results = True

        while has_more_results:

            url = self.address
            address = url + "p=" + str(page_idx) + "&"
            page = Webpage(address)
            if page.soup.ol.find_all('li'):
                #print page_idx
                #print address
                scrape_one_page(page.soup)
                page_idx += 1

            else:
                has_more_results = False

            #except AttributeError as e:
            #    print "AttributeError: {}".format(e)


def main():
    row = 2
    wb = ResultsSpreadsheet(filename="historicalSearchResults")
    wb.write_headers()

    query1 = RNCQueryAncient(lexi1="брати")

    search1 = RNCSearch(
        rnc_query=query1, subcorpus=u"Ancient", pfx_val=u"noPrefix",
        sfx_val=u"noSuffix", lem=u"брать", base_verb=u"брать")
    search1.addresses()
    search1.scrape_results_pages()

    for d in search1.all_search_results:
        for i in range(d[12]):
            wb.write_row(row_idx=row, dict_contents=d)
            row += 1

    query2 = RNCQueryAncient(lexi1="събирати")

    search2 = RNCSearch(
        rnc_query=query2, subcorpus=u"Ancient", pfx_val=u"yesPrefix",
        sfx_val=u"yesSuffix", lem=u"собирать", base_verb=u"брать")
    search2.addresses()
    search2.scrape_results_pages()

    for d in search2.all_search_results:
        for i in range(d[12]):
            wb.write_row(row_idx=row, dict_contents=d)
            row += 1

    #query2 = RNCQueryOld(req="брал")
    #query3 = RNCQueryModern(lex1="учитать")

    wb.save_wb()

    # vb = RussianVerb(simplex_verb="брать")

    ### print a list of prefixed forms of a verb
    #print "\nPrefixed forms list:\n"
    #for form in vb.prefixed_forms:
    #    print form,

    ### print a dictionary containing prefixed forms of a verb sorted by prefix
    #print "\nAll forms dict:\n"
    #for k, v in vb.all_forms_by_prefix.iteritems():
    #    print k
    #    for f in v:
    #        print "\t{}".format(f)

def main_real():
    row = 2
    wb = ResultsSpreadsheet(filename="historicalSearchResults")
    wb.write_headers()

    #vb1 = RussianVerb(simplex_verb="ждать")

    #for pfx, vb_list in vb1.all_forms_by_prefix.iteritems():
    #    for vb in vb_list:
    #        query = RNCQueryModern(lex1=vb)
    #
    #        pfxv = ''
    #        if pfx == '—':
    #            pfxv = "noPrefix"
    #        else:
    #            pfxv = "yesPrefix"
    #
    #        search = RNCSearch(
    #            rnc_query=query, subcorpus="Modern",
    #            pfx_val=pfxv, prefix=pfx, sfx_val="noSuffix",
    #            lem=vb, base_verb=vb1.root
    #            )
    #        search.addresses()
            #search.scrape_results_pages()
            #
            #for d in search.all_search_results:
            #    for i in range(d[12]):
            #        wb.write_row(row_idx=row, dict_contents=d)
            #        row += 1

            ## print all urls for results pages

    word = "почитывать"
    query = RNCQueryModern(lex1=word)
    search = RNCSearch(
        rnc_query=query, subcorpus="Modern",
        pfx_val="yesPrefix", prefix="po-",
        sfx_val="yesSuffix", suffix="-yva-",
        lem=word, base_verb="читать"
        )
    search.scrape()
    #search.addresses()
    #for idx, address in enumerate(search.results_page_urls):
    #    print "\n{}\n{}\n".format(idx, address)

#    query1 = RNCQueryAncient(lexi1="брати")
#
#    search1 = RNCSearch(
#        rnc_query=query1, subcorpus=u"Ancient", pfx_val=u"noPrefix",
#        sfx_val=u"noSuffix", lem=u"брать", base_verb=u"брать")
#    search1.addresses()
#    search1.scrape_results_pages()
#
#    for d in search1.all_search_results:
#        for i in range(d[12]):
#            wb.write_row(row_idx=row, dict_contents=d)
#            row += 1

    wb.save_wb()

if __name__ == "__main__":
    main_real()
