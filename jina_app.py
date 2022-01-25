import ast
import csv
from jina import Document, DocumentArray, DocumentArrayMemmap
from jina import Flow, Executor
from helper import SimpleIndexer, TextEncoder


def gen_docarray():
    docs = DocumentArray()

    with open("./data_finalize/lite_movies_metadata.csv", encoding="utf-8") as file:      # Complete dataset taking too much time to get indexed
        reader = csv.DictReader(file)
        movies = []

        for indx, row in enumerate(reader):
            # print(row.keys())
            movies.append(row['overview'])
            da = Document(text=row['overview']) #tags=ast.literal_eval(row['cast'])
            da.tags['genres'] = ast.literal_eval(row['genres'])
            da.tags['title'] = row['title']
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
        response = flow.post(on='/search', inputs = query, return_results = True)
    
    print("{} IS THE RESPONSE !!!".format(response))
    matches = response[0].docs[0].matches

    for ind, i in enumerate(matches):
        print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
        print(i.text)



def query_results(docs, query):
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
        response = flow.post(on='/search', inputs = query, return_results = True)
    
    recommended_movies = []
    print("{} IS THE RESPONSE !!!".format(response))
    matches = response[0].data.docs[0].matches

    for ind, i in enumerate(matches):
        print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
        recommended_movies.append(i.tags["title"])
        print(i.text)
        print()

    recommended_movies  = list(dict.fromkeys(recommended_movies))  #To remove the duplicates
    return recommended_movies       


if __name__ == "__main__":
    docs = gen_docarray()
    query = Document(text = input('Query movie: '))
    # indexnsearch(docs, query)

    query_results(docs, query)
