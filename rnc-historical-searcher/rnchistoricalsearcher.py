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
        pass

class RNCSearchAbstract(object):
    """Generic RNC search object."""

    def __init__(self):
        pass

class RNCSearchAncient(RNCSearchAbstract):
    """Search of the 'ancient' subcorpus of the Russian National Corpus."""

    def __init__(self):
        super(RNCSearchAncient, self).__init__()

class RNCSearchOld(RNCSearchAbstract):
    """Search of the 'old' subcorpus of the Russian National Corpus."""

    def __init__(self):
        super(RNCSearchOld, self).__init__()

class RNCSearchModern(RNCSearchAbstract):
    """Search of the 'modern' corpus of the Russian National Corpus"""

    def __init__(self):
        super(RNCSearchModern, self).__init__()

def main():
    pass

if __name__ == "__main__":
    main()
