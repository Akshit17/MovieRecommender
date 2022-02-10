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
            da = Document(text=row['overview']) 
            da.tags['genres'] = ast.literal_eval(row['genres'])
            da.tags['title'] = row['title']
            docs.append(da)
    docs.embeddings = stored_embeddings
  
    return docs


def query_results(docs):#, query):          #Uncomment if you wish to give queries from terminal instead of Web-app
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
        # flow.post(on='/index', inputs=docs, on_done=print)   #Uncomment this line to index the data (i.e if /workspace does not exist in your directory)
        flow.block()


if __name__ == "__main__":
    # os.system('rm -rf workspace')
    docs = gen_docarray()
    # query = Document(text = input('Query movie: '))   #Uncomment if you wish to give queries from terminal instead of Web-app
   
    query_results(docs)#, query)
