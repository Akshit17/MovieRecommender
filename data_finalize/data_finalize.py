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
for row in movies_metadata.iterrows:
    try:
        row['id'] = np.int64(row['id'])
    except:
        print("BEEP BOP")
        print(row['id'])
try:
    pd.to_numeric(movies_metadata.id)
except:
    movies_metadata = movies_metadata[movies_metadata.id!='1997-08-20']       #an exceptionally wrong id found manually in dataset
 
movies_metadata.head(10)
