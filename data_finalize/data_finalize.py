import numpy as np
import pandas as pd
import ast

def convert(obj):                         #function to get columns like 'genre' in desired format
    L = []
    try:
        for i in ast.literal_eval(obj):
            L.append(i['name'])
    except:
        pass
    return L


credits = pd.read_csv("./kaggle_moviedataset/credits.csv")
keywords = pd.read_csv("./kaggle_moviedataset/keywords.csv")
links_small = pd.read_csv("./kaggle_moviedataset/links_small.csv")
links = pd.read_csv("./kaggle_moviedataset/links.csv")
ratings_small = pd.read_csv("./kaggle_moviedataset/ratings_small.csv")
ratings = pd.read_csv("./kaggle_moviedataset/ratings.csv")
movies_metadata = pd.read_csv("./kaggle_moviedataset/movies_metadata.csv")


ml_25_genome_scores = pd.read_csv("./ml-25m/genome-scores.csv")
ml_25_genome_tags = pd.read_csv("./ml-25m/genome-tags.csv")
ml_25_links = pd.read_csv("./ml-25m/links.csv")
ml_25_movies= pd.read_csv("./ml-25m/movies.csv")
ml_25_ratings = pd.read_csv("./ml-25m/ratings.csv")
ml_25_tags = pd.read_csv("./ml-25m/tags.csv")


print(credits.head(10))
print(credits.info())
bool_series = credits.duplicated()         #series type
print(credits.duplicated().sum())
print(credits[bool_series])

# movies_metadata.info()
# movies_metadata['production_countries'].value_counts()
print(movies_metadata.iloc[0].genres)
#Genre is in not desired format 
# Need to convert "[{'id': 16, 'name': 'Animation'}, {'id': 35, 'name': 'Comedy'}, {'id': 10751, 'name': 'Family'}]" 
#  Into [ 'Animation', 'Comedy', 'Family']

movies_metadata.shape
movies_metadata.duplicated().sum()      #gave 13



movies_metadata = movies_metadata.sort_values(by="id")
print(type(movies_metadata['id'][0]))
#to merge the keywords.csv and movie_metadata.csv the id datatype should be same

# for row in movies_metadata.iterrows:
#     try:
#         row['id'] = np.int64(row['id'])
#     except:
#         print("BEEP BOP")
#         print(row['id'])
# try:
#     pd.to_numeric(movies_metadata.id)
# except:
#     movies_metadata = movies_metadata[movies_metadata.id!='1997-08-20']
# movies_metadata.head(4)

keywords = keywords.sort_values(by="id")
keywords['id'] = keywords['id'].astype(str)
# print(type(keywords['id'][0]))
# pd.to_numeric(keywords.id)
# keywords.head(4)

# movies_metadata = pd.concat([movies_metadata, keywords], axis=1)
movies_metadata = movies_metadata.merge(keywords , on="id")
# movies_metadata.head(10)
movies_metadata['genres'] = movies_metadata['genres'].apply(convert)
movies_metadata['keywords'] = movies_metadata['keywords'].apply(convert)
movies_metadata['production_companies'] = movies_metadata['production_companies'].apply(convert)
print(movies_metadata.head(10))


# movies_metadata.shape
credits = credits.sort_values(by="id")
credits['id'] = credits['id'].astype(str)


# movies_metadata = pd.concat([movies_metadata, credits], axis=1)
movies_metadata = movies_metadata.merge(credits , on="id")

print(movies_metadata.shape)

# movies_metadata.info()
print(movies_metadata['id'].value_counts())
print(movies_metadata["id"].nunique())
#handling duplicated data

print(movies_metadata[movies_metadata["id"].duplicated()])  #prints rows with duplicated attribute 'id'

movies_metadata = movies_metadata.drop_duplicates(subset=["id"] ,keep="first")
print(movies_metadata[movies_metadata["id"].duplicated()])
# movies_metadata["id"].nunique()   45432 unique which is equal to shp so all gud

movies_metadata = movies_metadata[["title","genres","imdb_id","id", "original_language",  "overview", "popularity" ,"poster_path", "production_companies", "production_countries" , "release_date", "revenue", "spoken_languages", "title", "video", "vote_average" , "vote_count" , "keywords" , "cast", "crew"]]

movies_metadata = movies_metadata.rename(columns={"id":"tmdb_id"})


movies_metadata.to_csv('movies_metadata.csv', index = False)


#TO-DO: From ml-25m dataset replace movieid with corresponding tmbd/imbd id

ml_25_movies = ml_25_movies.merge(ml_25_links , on="movieId")
print(type(ml_25_movies.iloc[0].genres))

print(ml_25_movies.iloc[0].genres)

def convert_ml_25m(obj):
    L = []
    print(obj)
    if obj == "(no genres listed)":          # Null values are listed in data in this format
        obj = None
    else:
        # print(type(obj))
        obj = obj.split('|')
        # print(obj)
    return obj
    
ml_25_movies['genres'] = ml_25_movies['genres'].apply(convert_ml_25m)
print(ml_25_movies)

ml_25_movies = ml_25_movies.dropna(subset=['genres'])    # Movie data with no genre is probably useless to train model over
print(type(ml_25_movies.iloc[0].genres))
print(ml_25_movies.shape)

ml_25_movies = ml_25_movies.rename(columns={"imdbId":"imdb_id" , "tmdbId":"tmdb_id"})

ml_25_movies.to_csv('ml_25_movies.csv', index = False)

# ml_25_movies.csv is missing few columns like 'overview' , 'cast', 'crew' when compared with movies_metadata.csv 

import imdb

moviesDB = imdb.IMDb()
