from distutils.log import debug
import flask
from flask import Flask, render_template, request
import csv
import pandas as pd

import jina_app
from jina import Document, DocumentArray, DocumentArrayMemmap
from jina import Flow, Executor

def get_suggestions():
    data = pd.read_csv('./data_finalize/movies_metadata.csv')
    return list(data['title'].str.capitalize())

def get_recommendations(movie_query):
    result = jina_app.query_results(movie_query)
    return result
    
# app = flask.Flask(__name__, template_folder='templates')

app = Flask(__name__, template_folder='static')
@app.route("/")
@app.route("/index")
def index():
   
    # movie_query = "Avengers"
    # recom_list = get_recommendations(movie_query)
    # #recom_list has list of all recommended movie titles use them to find other details from the csv
    # df = pd.read_csv("./data_finalize/movies_metadata.csv")
    # recom_df = df.loc[df['title'].isin(recom_list)]

    # names = []
    # overview=[]
    # mid=[]

    # if len(recom_list) == 0:
    #     return flask.render_template('Nota.html')
    # for i in range(len(recom_list)):
    #     names.append(recom_df.iloc[i][0])
    #     overview.append(recom_df.iloc[i][4])
    #     mid.append(recom_df.iloc[i][3])

    suggestions =   get_suggestions()      #get_suggestions
    
    return render_template('index.html',suggestions=suggestions) #,movieid=mid,movie_overview=overview,movie_names=names,search_name=movie_query)

# Set up the main route
@app.route('/positive', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        movie_query = flask.request.form['movie_name']
        movie_query = movie_query.title()
        # with open('movieR.csv', 'a',newline='') as csv_file:
        #     fieldnames = ['Movie']
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #     writer.writerow({'Movie': movie_query})
        docs = jina_app.gen_docarray()
        recom_list = jina_app.query_results(docs, movie_query)

        #recom_list has list of all recommended movie titles use them to find other details from the csv
        df = pd.read_csv("./data_finalize/movies_metadata.csv")
        recom_df = df.loc[df['title'].isin(recom_list)]

        names = []
        overview=[]
        mid=[]

        if len(recom_list) == 0:
            return flask.render_template('Nota.html')
        for i in range(len(recom_list)):
            names.append(recom_df.iloc[i][0])
            overview.append(recom_df.iloc[i][4])
            mid.append(recom_df.iloc[i][3])
            
        #render /positive page pls??
        return flask.render_template('Nota.html',movieid=mid,movie_overview=overview,movie_names=names,search_name=movie_query)

if __name__ == '__main__':
    app.run(debug=True)