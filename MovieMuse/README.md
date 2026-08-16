# MovieMuse

<p align="center">
  <a href="https://ibb.co/dsb6pwxq"><img src="https://i.ibb.co/CpJv93DZ/Chat-GPT-Image-Aug-14-2026-04-30-45-AM.png" alt="Chat-GPT-Image-Aug-14-2026-04-30-45-AM" border="0"></a>
</p>

> A command-line movie companion that learns what you like and helps you figure out what to watch next.

## About This Project

I built MovieMuse to get comfortable working with real external APIs, handling data that doesn't always come in clean, and putting together a full command-line app from scratch — not a script that runs once and prints an answer, but something you can actually open, use, and come back to.

It's a menu-driven Python program that talks to the TMDb API to pull real movie data, lets you log what you've watched and how much you liked it, and then uses that history to figure out your taste well enough to recommend what to watch next. It also remembers your API key and your favorite genres between runs, so setup only really happens once.

## Features

-  **Search any movie** — pulls the title, release date, genre, runtime, and plot straight from TMDb.
-  **Rate what you've watched** — rate on a 1–5 scale, with input validation so a stray "7" or a typo doesn't break the flow.
-  **Track your history** — every rating gets logged to a CSV file you can look back through anytime.
-  **Taste analysis** — looks at everything you rated 4 or higher, pulls each movie's real genre list from TMDb, and ranks which genres show up most. Your top genres get saved locally, so you don't have to re-run the analysis every session.
-  **Get recommendations** — converts your top genre(s) into TMDb's genre IDs and queries its `discover` endpoint directly, so you get movies that are actually tagged with that genre — not just titles that happen to contain the word.
-  **Remembers your API key** — enter it once on your first run, and it's saved locally for every run after that.

## How It Works

The whole thing runs on one main loop that routes you to whichever feature you pick:

1. On first run, you're asked for a TMDb API key, which gets validated with a quick request and saved to `apikey.txt`. Every run after that just reads the key back in, no re-entering needed.
2. Ratings are stored locally in `movie_rating.csv` — no database, which keeps the project lightweight and easy to inspect.
3. Taste analysis searches TMDb for each highly-rated movie by name to get its id, fetches its real genre list, and counts genre frequency using a plain dictionary and `sorted()`. The top genres get written to `favgenres.txt` so they persist even after you close the program.
4. Recommendations map genre names ("Thriller") to the numeric IDs TMDb actually requires (53) through a small lookup table, then query `discover/movie` with `with_genres` — genuine genre filtering, not a text search workaround.

## Tech Stack

- **Python 3**
- **[TMDb API](https://www.themoviedb.org/documentation/api)** — movie data source (search + discover endpoints)
- **requests** — handling the API calls
- **pandas** — filtering and working with the ratings data
- **csv** (standard library) — reading and writing the ratings log


## Example

```
            *Movie Recommendation System*

        1-Search Movies
        2-Rate for watched movies
        3-My Movies History
        4-Analyze My Taste
        5-Get recommendations
        6-Exit
Choose an option number: 
```

## Project Structure

```
moviemuse/
├── movie_recommender_tmdb.py   # main application
├── apikey.txt                  # created after your first run, stores your API key locally
├── favgenres.txt               # created after your first taste analysis, stores your top genres
├── movie_rating.csv            # created automatically after your first rating
├── requirements.txt
└── README.md
```

## What This Project Helped Me Practice

- Making real API requests and parsing JSON responses
- Working with two different REST APIs and seeing firsthand how differently two providers can model the same idea — "give me a movie's details" looks completely different depending on who you ask
- Multi-step API workflows (search by name to get an id, then fetch full details using that id)
- Reading and writing both CSV and plain text files to persist different kinds of local state
- Using pandas to filter and work with tabular data
- Writing input-validation loops that don't crash on bad input
- Structuring a multi-feature CLI app around a single menu loop
- Basic data analysis logic — counting and ranking genre frequency by hand
- Debugging state that persists across runs, including the kind of bug that only shows up the *second* time you run the program, not the first
