
# About
- Quranfal is a Quran web application written in django and aims to facilitate learning Quran's language while reading it.
- Currently live at [www.quranicjourney.com](quranicjourney.com)

# Features
- Mark known words and get a report of its frequency in Quran, and what percentage of Quran is understood. 
- Add unknown words to 'study' list
- Flash card tool to study words added to 'study' list
- Click on a word to see all of its occurrences in Quran
- See morphological information of the words (data from quran.corpus.com). Click on its lemma, to see all related words and ayas in the Quran. Similarly, click on its root, to see all related lemmas, words and ayas. 
- Word by word meaning (English only for now)
- Several translations 
- Settings organized as beginner-intermediate-advanced

# To Do
- Add grammatical information related to morphological structures
- Quranic word's relatives in other languages
- Add tafseer
- Add tafseer (user contributions)
- Add word-by-word meanings and translations in other languages
- A regexp tool to filter or highlight certain language constructs

# Installation
1. Install Vagrant + VirtualBox
1. Download [django-quran](http://github.com/doganmeh/django-quran/) and place in the directory that you put quranfal
1. From terminal go to quranfalweb/vm/dev
1. Issue command: `vagrant up`
1. Project running at 127.0.0.1:8080
1. If for any reason Quran data does not load automatically, issue these two commands in project root:
    1. `python manage.py migrate`
    1. `python manage.py load_all`