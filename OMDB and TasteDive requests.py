import requests_with_caching
import json
#Fetching data from the tasteDive API
def get_movies_from_tastedive(movie_name):
    params={}
    params["q"]=movie_name
    params["type"]="movies"
    params["limit"]=5
    baseurl="https://tastedive.com/api/similar"
    response=requests_with_caching.get(baseurl,params)
    data=json.loads(response.text)
    return data 

def extract_movie_titles(dictionnary):
    titles_movies=[]
    for movie in dictionnary["Similar"]["Results"]:
        titles_movies.append(movie["Name"])
    return titles_movies

def get_related_titles(related_titles):
    if related_titles!=[]:
        movies_related_list=[]
        extracted_movies_related_list=[]
        for Movie_name in related_titles:
            movies_related_list=extract_movie_titles(get_movies_from_tastedive(Movie_name))
            for Movie_related in movies_related_list:
                if Movie_related not in extracted_movies_related_list:
                    extracted_movies_related_list.append(Movie_related)
        return extracted_movies_related_list
    else:
        return []
    
#Fetching data from the OMDB
def get_movie_data(Movie_title):
    baseurl="http://www.omdbapi.com/"
    params={}
    params["t"]=Movie_title
    params["r"]="json"
    response=requests_with_caching.get(baseurl,params)
    print(response.url)
    print(type(response))
    data=response.json()
    print(type(data))
    return data
data=get_movie_data("Venom")
print(data)

def get_movie_rating(title_dict):
    rates=""
    for rate in title_dict["Ratings"]:
        if rate["Source"]=='Rotten Tomatoes':
            rates=rate["Value"]
            print(rates)
    if rates!="":
        int_rate=int(rates[:2])
    else:
        int_rate=0
    return int_rate
print(get_movie_rating(get_movie_data("Deadpool 2")))

#the main program

def get_sorted_recommendations(titles):
    title_list = get_related_titles(titles)
    title_list = sorted(title_list, key = lambda title: (get_movie_rating(get_movie_data(title)), title), reverse=True)
    
    return title_list

    
    