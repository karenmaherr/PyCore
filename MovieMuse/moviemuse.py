import requests
import pandas as pd
import csv
import os
favorite_genre1 = None
favorite_genre2 = None
apikey=input(" Enter your api key for OMDB :")
while True:
    print("""
            *Movie Recomindation System*        

        1-Search Movies
        2-Rate for watched movies
        3-My Movies History 
        4-Analyze My Taste
        5-Get recommendations
        6-Exit""")
    ans= input(" Choose an option number :")
    if ans=="6":
        break
    if ans=="1":
        movie=input(" Enter the movie name :")
        url =f"http://www.omdbapi.com/?apikey={apikey}&t={movie}"
        response=requests.get(url)
        data= response.json()
        if data["Response"]=="True":
            print(data["Title"])
            print(data["Year"])
            print(data["Rated"])
            print(data["Released"])
            print(data["Genre"])
            print(data["Runtime"])
            print(data["Plot"])
        else:
            print("Movie not found")
    elif ans=="2":
        rate=float(input(" Enter your rate for the movie from 1 to 5 :"))
        while rate<1 or rate>5:
            rate=float(input(" Please enter your rate from 1 to 5 only :"))
        movie=input("Enter the movie name: ")
        file_exists=os.path.exists("movie_rating.csv")
        with open ("movie_rating.csv","a",newline="")as file:
            writer=csv.writer(file)
            if not file_exists:
                writer.writerow(["movie","rate"])
            writer.writerow([movie,rate])
        print("Rate saved !")
    elif ans=="3":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
            
        else:
            with open ("movie_rating.csv","r")as file:
                reader=csv.reader(file)
                for row in reader:
                    print(row)
    elif ans=="4":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
            
        else:
            df=pd.read_csv("movie_rating.csv")
            favorite_movies=df[df["rate"]>=4]
            genre_count={}
            for movie in favorite_movies["movie"]:
                url =f"http://www.omdbapi.com/?apikey={apikey}&t={movie}"
                response=requests.get(url)
                data= response.json()
                if data["Response"]=="True":
                    genres=data["Genre"].split(",")
                    for genre in genres:
                        genre=genre.strip()
                        if genre in genre_count:
                            genre_count[genre]+=1
                        else:
                            genre_count[genre]=1
            print(" Your Taste Analysis \n")

            sorted_genres = sorted(
                genre_count,
                key=genre_count.get,
                reverse=True)
            if len(sorted_genres)==0:
                print("You didn't rate enough movies with genres")
            else:
                print("You seem to love :\n")
                for i, genre in enumerate(sorted_genres, 1):
                    print(f"{i}. {genre}")
                print(" Your favorite genre:", sorted_genres[0])
                favorite_genre1=sorted_genres[0]
                if len(sorted_genres)>1:
                    favorite_genre2=sorted_genres[1]
                    favorite_genre2="True"
                else:
                    favorite_genre2="False"
    elif ans=="5":
        if not os.path.exists("movie_rating.csv"):
            print("You didn't watch any movie")
        elif not favorite_genre1:
            print("You didn't rate enough movies")
        else:
            print("  Your top recommendations based on your favourite genres"    )
            url1 =f"http://www.omdbapi.com/?apikey={apikey}&s={favorite_genre1}"
            url2 =f"http://www.omdbapi.com/?apikey={apikey}&s={favorite_genre2}"
            response1=requests.get(url1)
            data1= response1.json()
            response2=requests.get(url2)
            data2= response2.json()
            if data1["Response"]=="True" and data2["Response"]=="True":
                n1=len(data1["Search"])
                n2=len(data2["Search"])
                for r in range(10):
                    if r<n1:
                        print(data1["Search"][r]["Title"])
                    if r<n2:
                        if favorite_genre2=="True":
                            print(data2["Search"][r]["Title"])        
            else:
                print("No movies found")
