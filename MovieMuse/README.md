#  MovieMuse

<p align="center">
  <a href="https://ibb.co/dsb6pwxq"><img src="https://i.ibb.co/CpJv93DZ/Chat-GPT-Image-Aug-14-2026-04-30-45-AM.png" alt="Chat-GPT-Image-Aug-14-2026-04-30-45-AM" border="0"></a>
</p>


## About This Project

I built MovieMuse to get comfortable working with a real external API, handling data that doesn't always come in clean, and putting together a full command-line app from scratch — not a script that runs once and prints an answer, but something you can actually open, use, and come back to.

It's a menu-driven Python program that talks to the IMDB API to pull real movie data, lets you log what you've watched and how much you liked it, and then uses that history to figure out your taste well enough to suggest what to watch next.

## Features

-  **Search any movie** — pulls the title, year, release date, genre, runtime, and plot straight from IMDB.
-  **Rate what you've watched** — rate on a 1–5 scale, with input validation so a stray "7" or a typo doesn't break the flow.
-  **Track your history** — every rating gets logged to a CSV file you can look back through anytime.
-  **Taste analysis** — looks at everything you rated 4 or higher, pulls each movie's genre from the API, and ranks which genres show up most.
-  **Get recommendations** — takes your top genre(s) and searches IMDB for related titles, so you're not stuck guessing.

## How It Works

The whole thing runs on one main loop that routes you to whichever feature you pick:

1. Every action goes through a single menu (search / rate / history / analyze / recommend / exit).
2. Ratings are stored locally in `movie_rating.csv` — no database, which keeps the project lightweight and easy to inspect (you can just open the file and see your own data).
3. Taste analysis re-queries IMDB for the genre of every highly-rated movie, then counts genre frequency using a plain dictionary and `sorted()` — no extra library needed for the ranking itself.
4. Recommendations use your top genre(s) as search terms against IMDB's search endpoint.

## Tech Stack

- **Python 3**
- **[IMDB API](https://www.imdbapi.com/)** — movie data source
- **requests** — handling the API calls
- **pandas** — filtering and working with the ratings data
- **csv** (standard library) — reading and writing the ratings log
 
## Example

```
            *Movie Recommendation System*        

        1-Search Movies
        2-Rate for watched movies Movies
        3-My Movies History 
        4-Analyze My Taste
        5-Get recommendations
        6-Exit
 Choose an option number :
```

## Project Structure

```
moviemuse/
├── movie_recommender.py   # main application
├── movie_rating.csv       # created automatically after your first rating
├── requirements.txt
└── README.md
```

## What This Project Helped Me Practice

- Making real API requests and parsing JSON responses
- Reading and writing CSV files for persistent local storage
- Using pandas to filter and work with tabular data
- Writing input-validation loops that don't crash on bad input
- Structuring a multi-feature CLI app around a single menu loop
- Basic data analysis logic — counting and ranking genre frequency by hand
