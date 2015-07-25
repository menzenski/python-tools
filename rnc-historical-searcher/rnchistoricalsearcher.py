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
import re

## TODO: Rewrite this as a "RNCSource" class with a date() method (Should I?)
def source_date(full_source_name_as_string):
    """Return numerical date ranges from source name string."""

    # if date is provided in parentheses (most common)
    if re.findall('\(.*?\)', full_source_name_as_string):
        date_string = re.findall('\(.*?\)', full_source_name_as_string)

        ## TYPE (1400-1500), (1441-1442)
        if re.findall('\A\d{4}-\d{4}\Z', date_string[0][1:-1]):
            dates = re.findall('\A\d{4}-\d{4}\Z', date_string[0][1:-1])
            date_begin = int(dates[0].split("-")[0])
            date_end = int(dates[0].split("-")[1])
            date_middle = (date_begin + date_end) / 2.0

        ## TYPE (1550), (1570)
        elif len(date_string) == 6:
            date_year = int(re.findall('\A\d{4}\Z', date_string[0][1:-1])[0])
            date_begin = date_year
            date_middle = date_year
            date_end = date_year

        ## TYPE (1423.02.20), (1436.06.13)
        elif len(date_string) == 12:
            date_year = int(re.findall('\A\d{4}', date_string[0][1:-1])[0])
            date_begin = date_year
            date_middle = date_year
            date_end = date_year

        ## TODO: Is this elif clause captured by the next one? (Yes?)
        # date possibly in another format
        elif re.findall('\d{4}', date_string[0])[0]:
            date_year = int(re.findall('\d{4}', date_string[0])[0])
            date_begin = date_year
            date_middle = date_year
            date_end = date_year

    # if date is given outside parentheses (less common)
    elif re.findall('\d{4}', full_source_name_as_string):
        date_string = re.findall('\d{4}', full_source_name_as_string)
        date_begin = int(date_string[0])
        date_middle = int(date_string[0])
        date_end = int(date_string[0])

    # if date not given at all (common for earliest texts)
    else:
        date_begin, date_middle, date_end = 0, 0, 0
        print "No date found"

    ## TODO: Make this not return a tuple (i.e., rewrite function as class)
    return date_begin, date_middle, date_end


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

class RNCSearchTerm(object):
    """Object containing all (past-tense) forms of a search term."""

    def __init__(self):
        self.ancient_simplex = {}

class RNCSearchAncient(object):
    """Search of the 'ancient' subcorpus of the Russian National Corpus."""

    def __init__(self):
        pass

class RNCSearchOld(object):
    """Search of the 'old' subcorpus of the Russian National Corpus."""

    def __init__(self):
        pass

class RNCSearchModern(object):
    """Search of the 'modern' corpus of the Russian National Corpus"""

    def __init__(self):
        pass

def main():
    sources = [
        "Неизвестный. Модест и София (1810) ",
        "К нашему любимому празднику: все угощенье -- на стол! // «Даша», 2004",
        "Ирина Гнатюк. Найден источник горячей воды (2003) // «Богатей» (Саратов), 2003.05.22",
        "Бельский летописец (1630-1635)",
        "Летописец 1619-1691 гг (1692) ",
        "Киевская летопись",
        "Шамиль Аляутдинов. Мусульмане: кто они? (1997-1999)",
        "Киевская летопись (1623.03.04)",
        ]
    for source in sources:
        print source,
        print source_date(source)

if __name__ == "__main__":
    main()
