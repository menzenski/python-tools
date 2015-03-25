#! /usr/bin/env python
# -*- coding: utf-8 -*-

##########
## textsplitter.py Version 1.0 (2015-03-23)
##
## Original author: Matthew Menzenski (menzenski@ku.edu)
##
## License: CC-BY-4.0 ( https://creativecommons.org/licenses/by/4.0/ )
##########

import itertools as it
import math

filename = 'WarAndPeaceEnglish.txt'

chapter_counter = -0.5

with open(filename,'r') as f:
    for key,group in it.groupby(f,lambda line: line.startswith('@\n')):
        chapter_counter += 0.5
        if len(str(math.trunc(chapter_counter))) == 1: 
            chapter_filename = "Chapter00{chap}.txt".format(
                chap=math.trunc(chapter_counter))
        elif len(str(math.trunc(chapter_counter))) == 2: 
            chapter_filename = "Chapter0{chap}.txt".format(
                chap=math.trunc(chapter_counter))
        elif len(str(math.trunc(chapter_counter))) == 3: 
            chapter_filename = "Chapter{chap}.txt".format(
                chap=math.trunc(chapter_counter))
        else:
            print "whoops!"
        if not key:
            with open(chapter_filename, 'a') as stream:
                for line in group:
                    stream.write(line)
