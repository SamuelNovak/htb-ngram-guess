# N-gram guesser

*Author: Samuel Novák* (s1865783 *at* sms *dot* ed *dot* ac *dot* uk ***:P***)

A game where you guess which one of four given word combinations was the most commonly occuring in a specified year, according to the language corpora accessed by the [Google Books Ngram Viewer](https://books.google.com/ngrams). This game is played over the mobile network, using the the [Nexmo Voice API](https://www.nexmo.com/).

For now, these are adjective-noun pairs, but it could easily be extended to anything that Google Ngram can handle.

## Technologies used

* Python 3 - language of choice
* Python Flask - web application framework
* PostgreSQL - database
* Psycopg2 - PostgreSQL driver for Python
---
* Google Ngram Viewer - source of the data used to generate riddles
* Nexmo Voice API - mobile network communication
* Google Cloud Compute Engine - backend server

I... *think* that's all. *(?)*