# N-gram guesser

*Solo project from Hack The Burgh V (2019)*

A game where you guess which one of four given word combinations was the most commonly occuring in a specified year, according to the language corpora accessed by the [Google Books Ngram Viewer](https://books.google.com/ngrams). This game is played over the mobile network, using the the [Nexmo Voice API](https://www.nexmo.com/).

For now, these are adjective-noun pairs, but it could easily be extended to anything that Google Ngram can handle.

The game stores the number of points a player (identified by their telephone number) has in a PostgreSQL database and also has a leaderboard accessible on the website.

## How to play

Simply call the number and follow the instructions ;)
*Note: The game is not currently running.*

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
