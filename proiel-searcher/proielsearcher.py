#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## proielsearcher.py Version 1.0 (2015-02-17)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: CC-BY-4.0 ( https://creativecommons.org/licenses/by/4.0/ )
##########

from bs4 import BeautifulSoup
import codecs
import urllib
import sgmllib
import lxml.html

class OldChurchSlavicWord(object):
    """
    An Old Church Slavic word in the PROIEL corpus.
    """

    def __init__(self, word):
        self.word = word
