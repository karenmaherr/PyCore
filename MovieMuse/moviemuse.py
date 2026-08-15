import requests
import pandas as pd
import csv
import os

favorite_genre1 = None
favorite_genre2 = None
favorite_genre3 = None
favorite_genre22 = False
favorite_genre33 = False
GENRE_MAP = {
    "Action": 28, "Adventure": 12, "Animation": 16, "Comedy": 35,
    "Crime": 80, "Documentary": 99, "Drama": 18, "Family": 10751,
    "Fantasy": 14, "History": 36, "Horror": 27, "Music": 10402,
    "Mystery": 9648, "Romance": 10749, "Science Fiction": 878,
    "TV Movie": 10770, "Thriller": 53, "War": 10752, "Western": 37}
while True:
    apikey = input("Enter your API key for TMDB: ")
    response = requests.get(f"https://api.themoviedb.org/3/movie/550?api_key={apikey}")
    data = response.json()
    if response.status_code == 200:
        break
    print("Enter a valid API key")
while True:
    print("""
            *Movie Recommendation System*
        
        1-Search Movies
        2-Rate for watched movies
        3-My Movies History
        4-Analyze My Taste
        5-Get recommendations
        6-Exit""")
    ans = input("Choose an option number: ")
    if ans == "6":
        break
    if ans == "1":
        movie = input("Enter the movie name: ")
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={apikey}&query={movie}"
        search_response = requests.get(search_url)
        search_data = search_response.json()
        if search_data.get("results"):
            movie_id = search_data["results"][0]["id"]
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apikey}"
            response = requests.get(url)
            data = response.json()
            if response.status_code == 200:
                print(data["title"])
                print(data["release_date"])
                print(data["genres"][0]["name"])
                print(data["runtime"]+str("m"))
                print(data["overview"])
            else:
                print("Movie not found")
        else:
            print("Movie not found")
    elif ans == "2":
        movie = input("Enter the movie name: ")
        rate = float(input("Enter your rate for the movie from 1 to 5: "))
        while rate < 1 or rate > 5:
            rate = float(input("Please enter your rate from 1 to 5 only: "))
        file_exists = os.path.exists("movie_rating.csv")
        with open("movie_rating.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["movie", "rate"])
            writer.writerow([movie, rate])
        print("Rate saved!")
    elif ans == "3":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
        else:
            with open("movie_rating.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    print(row)
    elif ans == "4":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
        else:
            df = pd.read_csv("movie_rating.csv")
            favorite_movies = df[df["rate"] >= 4]
            genre_count = {}
            for movie in favorite_movies["movie"]:
                search_url = f"https://api.themoviedb.org/3/search/movie?api_key={apikey}&query={movie}"
                search_response = requests.get(search_url)
                search_data = search_response.json()
                if search_data.get("results"):
                    movie_id = search_data["results"][0]["id"]
                    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apikey}"
                    response = requests.get(url)
                    data = response.json()
                    if response.status_code == 200:
                        genres = data["genres"]
                        for genre in genres:
                            genre = genre["name"]
                            if genre in genre_count:
                                genre_count[genre] += 1
                            else:
                                genre_count[genre] = 1
            print("Your Taste Analysis\n")
            sorted_genres = sorted(genre_count, key=genre_count.get, reverse=True)
            if len(sorted_genres) == 0:
                print("You didn't rate enough movies with genres")
            else:
                print("You seem to love:\n")
                for i, genre in enumerate(sorted_genres, 1):
                    print(f"{i}. {genre}")
                print("Your favorite genre:", sorted_genres[0])
                favorite_genre1 = sorted_genres[0]
                genre_id1 = GENRE_MAP.get(favorite_genre1)
                if len(sorted_genres) > 1:
                    favorite_genre2 = sorted_genres[1]
                    favorite_genre22 = True
                    genre_id2 = GENRE_MAP.get(favorite_genre2)
                if len(sorted_genres) > 2:
                    favorite_genre3 = sorted_genres[2]
                    favorite_genre33 = True
                    genre_id3 = GENRE_MAP.get(favorite_genre3)
    elif ans == "5":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
        elif not favorite_genre1:
            print("You didn't rate enough movies")
        else:
            print("Your top recommendations based on your favourite genres \n")
            url1 = f"https://api.themoviedb.org/3/discover/movie?api_key={apikey}&with_genres={genre_id1}&sort_by=popularity.desc"
            if favorite_genre22:
                url2 = f"https://api.themoviedb.org/3/discover/movie?api_key={apikey}&with_genres={genre_id2}&sort_by=popularity.desc"
                response2 = requests.get(url2)
                data2 = response2.json()
                if response2.status_code == 200:
                    n2 = len(data2["results"])
            if favorite_genre33:
                url3 = f"https://api.themoviedb.org/3/discover/movie?api_key={apikey}&with_genres={genre_id3}&sort_by=popularity.desc"
                response3 = requests.get(url3)
                data3 = response3.json()
                if response3.status_code == 200:
                    n3 = len(data3["results"])
            response1 = requests.get(url1)
            data1 = response1.json()
            if response1.status_code == 200:
                n1 = len(data1["results"])
                for r in range(100):
                    if r < n1:
                        print(data1["results"][r]["title"])
                    if r < n2 and favorite_genre22:
                        print(data2["results"][r]["title"])
                    if r < n3 and favorite_genre33:
                        print(data3["results"][r]["title"])
            else:
                print("No movies found")
    else:
        print("Please choose a valid option")
