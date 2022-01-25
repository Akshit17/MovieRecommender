import flask
from flask import Flask, render_template, request
import csv
import pandas as pd

import jina_app

def get_suggestions():
    data = pd.read_csv('./data_finalize/movies_metadata.csv.csv')
    return list(data['title'].str.capitalize())

def get_recommendations(movie_query):
    result_final = jina_app.query_results(movie_query)
    


app = flask.Flask(__name__, template_folder='templates')

app = Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
    NewMovies=[]
    with open('movieR.csv','r') as csvfile:
        readCSV = csv.reader(csvfile)
        NewMovies.append(random.choice(list(readCSV)))
    movie_query = NewMovies[0][0]
    movie_query = movie_query.title()
    
    with open('movieR.csv', 'a',newline='') as csv_file:
        fieldnames = ['Movie']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'Movie': movie_query})
        recom_list = get_recommendations(movie_query)
        names = []
        dates = []
        ratings = []
        overview=[]
        types=[]
        mid=[]
        for i in range(len(recom_list)):
            names.append(recom_list.iloc[i][0])
            dates.append(recom_list.iloc[i][1])
            ratings.append(recom_list.iloc[i][2])
            overview.append(recom_list.iloc[i][3])
            types.append(recom_list.iloc[i][4])
            mid.append(recom_list.iloc[i][5])
    suggestions =   get_suggestions()      #get_suggestions
    
    return render_template('index.html',suggestions=suggestions,movie_type=types[5:],movieid=mid,movie_overview=overview,movie_names=names,movie_date=dates,movie_ratings=ratings,search_name=m_name)

# Set up the main route
@app.route('/positive', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        movie_query = flask.request.form['movie_name']
        movie_query = movie_query.title()
        with open('movieR.csv', 'a',newline='') as csv_file:
            fieldnames = ['Movie']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Movie': movie_query})
        recom_list = jina_app.query_results(movie_query)

        #recom_list has list of all recommended movie titles use them to find other details from the csv
        names = []
        dates = []
        ratings = []
        overview=[]
        types=[]
        mid=[]
        if len(recom_list) == 0:
            return flask.render_template('Nota.html')
        for i in range(len(recom_list)):
            names.append(recom_list.iloc[i][0])
            dates.append(recom_list.iloc[i][1])
            ratings.append(recom_list.iloc[i][2])
            overview.append(recom_list.iloc[i][3])
            types.append(recom_list.iloc[i][4])
            mid.append(recom_list.iloc[i][5])
            
        return flask.render_template('positive.html',movie_type=types[5:],movieid=mid,movie_overview=overview,movie_names=names,movie_date=dates,search_name=movie_query)

if __name__ == '__main__':
    app.run()