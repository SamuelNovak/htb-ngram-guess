# N-gram guesser

*Author: Samuel Novák* (s1865783 *at* sms *dot* ed *dot* ac *dot* uk ***:P***)

Website: http://35.230.134.67

A game where you guess which one of four given word combinations was the most commonly occuring in a specified year, according to the language corpora accessed by the [Google Books Ngram Viewer](https://books.google.com/ngrams). This game is played over the mobile network, using the the [Nexmo Voice API](https://www.nexmo.com/).

For now, these are adjective-noun pairs, but it could easily be extended to anything that Google Ngram can handle.

The game stores the number of points a player (identified by their telephone number) has in a PostgreSQL database and also has a leaderboard accessible on the website.

## How to play

Simply call the number **+44 752 063 5242** and follow the instructions ;)

## Technologies used

* Python 3 - language of choice
* Python Flask - web application framework
* PostgreSQL - database for player points storage
* Psycopg2 - PostgreSQL driver for Python
* HTML + JS - simple web frontend with leaderboard
---
* Google Ngram Viewer - source of the data used to generate riddles
* Nexmo Voice API - mobile network communication
* Google Cloud Compute Engine - backend server
