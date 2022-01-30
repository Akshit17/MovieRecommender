import ast
import os
import csv
import pickle
from jina import Document, DocumentArray, DocumentArrayMemmap
from jina import Flow, Executor
from helper import SimpleIndexer, TextEncoder



def gen_docarray():
    docs = DocumentArray()


    with open('./data_finalize/embeddings.pkl', "rb") as fIn:
        stored_data = pickle.load(fIn)
        stored_sentences = stored_data['sentences']
        stored_embeddings = stored_data['embeddings']

    with open("./data_finalize/movies_metadata.csv", encoding="utf-8") as file:      # Complete dataset taking too much time to get indexed
        reader = csv.DictReader(file)
        movies = []

        for indx, row in enumerate(reader):
            # print(row.keys())
            movies.append(row['overview'])
            da = Document(text=row['overview']) #tags=ast.literal_eval(row['cast'])
            da.tags['genres'] = ast.literal_eval(row['genres'])
            da.tags['title'] = row['title']
            da.embeddings = stored_embeddings[indx]
            docs.append(da)
    # d.plot('document.svg') for d in docs
    # print(type(docs.get_vocabulary()))
    print(docs[0].json())
    return docs

def indexnsearch(docs, query):
    flow = (
        Flow(cors=True)
        .add(
        name='text_encoder',
        uses=TextEncoder,
        )
        .add(
            name='simple_indexer',
            uses=SimpleIndexer,
            uses_metas={"workspace": "workspace/indexing"},
            volumes="./workspace:/workspace/indexing",
        )
    )   
    
    flow.plot('flow.svg')
    with flow:
        flow.post(on='/index', inputs=docs, on_done=print)
    
    with flow:    
        # response = flow.post(on='/search', inputs = query, return_results = True)
        response = flow.post(on='/search', inputs = DocumentArray([Document(text=query)]), return_results = True)
    
    print("{} IS THE RESPONSE !!!".format(response))
    matches = response[0].docs[0].matches

    for ind, i in enumerate(matches):
        print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
        print(i.text)


def search_results(docs, query):
    flow = (
        Flow(cors=True, protocol='http', port_expose=34567)
        .add(
        name='text_encoder',
        uses=TextEncoder,
        )
        .add(
            name='simple_indexer',
            uses=SimpleIndexer,
            uses_metas={"workspace": "workspace/indexing"},
            volumes="./workspace:/workspace/indexing",
        )
    )   

    with flow:    
        # response = flow.post(on='/search', inputs = query, return_results = True)
        response = flow.post(on='/search', inputs = DocumentArray([Document(text=query)]), return_results = True)
        print(response)

        recommended_movies = []
        print("{} IS THE RESPONSE !!!".format(response))
        matches = response[0].data.docs[0].matches

        for ind, i in enumerate(matches):
            print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
            recommended_movies.append(i.tags["title"])
            print(i.text)
            print()

        recommended_movies  = list(dict.fromkeys(recommended_movies))  #To remove the duplicates
        print(recommended_movies)
        flow.block()
        print("YOU MADE IT OUT OF FLOW.BLOCK(1111111)?!")
    print("YOU MADE IT OUT OF FLOW.BLOCK(222222222)?!")

def query_results(docs):#, query):
    flow = (
        Flow(cors=True, protocol='http', port_expose=34567)
        .add(
        name='text_encoder',
        uses=TextEncoder,
        )
        .add(
            name='simple_indexer',
            uses=SimpleIndexer,
            uses_metas={"workspace": "workspace/indexing"},
            volumes="./workspace:/workspace/indexing",
        )
    )   

    flow.plot('flow.svg')

    with flow:
        flow.post(on='/index', inputs=docs, on_done=print)
        flow.block()

    # with flow: 
    #     flow.block()

    # with flow:    
    #     print(flow.protocol) #= 'http'
    #     print(flow.port_expose) #= 34567
    #     print("{} is query and {} is its type".format(query, type(query)) )
    #     response = flow.post(on='/search', inputs = query, return_results = True)

        # response = flow.post(on='/search', inputs = DocumentArray([Document(text=query)]), return_results = True)
            # response = requests.post('http://127.0.0.1:34567/search', inputs = query)
            # res = response.json()
            # return_text = res["data"]['docs'][0]['matches'][0]
            # print("return_text is {}".format(return_text))
    # flow.block()
'''     '''
    # recommended_movies = []
    # print("{} IS THE RESPONSE !!!".format(response))
    # matches = response[0].data.docs[0].matches

    # for ind, i in enumerate(matches):
    #     print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
    #     recommended_movies.append(i.tags["title"])
    #     print(i.text)
    #     print()

    # recommended_movies  = list(dict.fromkeys(recommended_movies))  #To remove the duplicates
    # return recommended_movies       
'''     '''

if __name__ == "__main__":
    os.system('rm -rf workspace')
    docs = gen_docarray()
    # query = Document(text = input('Query movie: '))
    # # indexnsearch(docs, query)

    query_results(docs)#, query)
