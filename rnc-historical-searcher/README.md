# RNC Historical Searcher

This repository contains Python tools for searching the historical
subcorpora of the Russian National Corpus. Specifically, these scripts
return the number of occurrences by year and by source for given verb forms.

The `ancientrussiansearcher.py` script searches the
[древнерусский подкорпус / Ancient Russian subcorpus](http://ruscorpora.ru/search-old_rus.html),
while `oldrussiansearcher.py` searches the
[старорусский подкорпус / Old Russian subcorpus](http://ruscorpora.ru/search-mid_rus.html). There
are two scripts which search the
[основной корпус / Main corpus](http://ruscorpora.ru/search-main.html),
`modernrussiansearcherto1799.py` and
`modernrussiansearcher1800to1899.py`. They're separate files because at
first I wasn't interested in data later than 1800. I might combine
them. (I might actually try to combine all the scripts into one
general search tool, but that's a project for a later time.)

### License

Unless otherwise indicated, everything here is shared under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
