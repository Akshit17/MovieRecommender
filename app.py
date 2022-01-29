# from distutils.log import debug
# from urllib import response
# from fastapi import requests
import requests
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
      
        # docs = jina_app.gen_docarray()

        # jina_app.query_results(docs , movie_query)
        # jina_app.search_results(docs , movie_query)
        # print("YOU MADE IT OUT OF FLOW.BLOCK()?!")
        # recom_list = jina_app.query_results(docs, movie_query)

        response = requests.post(url="http://0.0.0.0:34567/search", data=movie_query)
        print("HERE IS THE FLASK RESPONSE:-")
        print(response)
        # print(response.json())
        # res = response.json()
        # print(res['data']['docs'][0]['matches'][0])


        headers = {
        'Content-Type': 'application/json',
        }
        data = '{"top_k":10,"mode":"search","data":["' + movie_query + '"]}'
        response = requests.post('http://10.0.2.15:34567/search', headers=headers, data=data)
        res = response.json()
        for i in range (0,10):
            print(res['data']['docs'][0]['matches'][i]['tags']['title'])


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
            
        #render /positive page pls??
        # return flask.render_template('index.html',movieid=mid,movie_overview=overview,movie_names=names,search_name=movie_query)
        return flask.render_template('Nota.html')

if __name__ == '__main__':
    app.run(debug=True)