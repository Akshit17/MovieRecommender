import numpy as np
import pandas as pd
import ast

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