from flask import Flask,redirect,url_for,render_template,request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import bs4 as bs
import urllib.request
import pickle
import requests
from tmdbv3api import TMDb
import json
from tmdbv3api import Movie
tmdb_movie = Movie()

file = open("./key.json",'r')
json_file = json.load(file)
api_key = json_file['api_key']

tmdb = TMDb()
tmdb.api_key = api_key

def create_similarity():
    data = pd.read_csv('./clean_dataset/main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity
def recommendation(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return('Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l    

app=Flask(__name__)
def get_genre(x):
    genres=[]
    result = tmdb_movie.search(x)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    poster = data_json['poster_path']
    if data_json['genres']:
        genre_str = " " 
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
        return genre_str.join(genres),poster
    else:
        return(None,poster)
@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        movie = request.form['movie']
        print(movie)
        genre_list = []
        posters = []
        rmd = recommendation(movie)
        for m in rmd:
            g,p = get_genre(m)
            genre_list.append(g)
            posters.append(p)
        # Handle POST Request here
        return render_template('recommendation.html',movie=movie,details = zip(rmd,genre_list,posters))
    return render_template('home.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)