import sys
import os
import ast
import csv
from jina import Document, DocumentArray, DocumentArrayMemmap
from jina import Flow, Executor
from helper import SimpleIndexer, TextEncoder

# da = DocumentArray.load_csv("./movies_metadata.csv")
#UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 455: character maps to <undefined>


# da = DocumentArray.load_csv("./movies_metadata.csv", encoding="utf8")
#gives error with encoding .  No attribute named 'encoding' either to specify encoding or to use utf8

docs = DocumentArray()

with open("./data_finalize/movies_metadata.csv", encoding="utf-8") as file:
    #setup csv reader
    reader = csv.DictReader(file)
    #setup list to hold dictionaries
    movies = []
    #loop through each row in the csv
    for row in reader:
        # print(row.keys())
        #append each row to the list
        movies.append(row['overview'])
        da = Document(text=row['overview']) #tags=ast.literal_eval(row['cast'])
        da.tags['genres'] = ast.literal_eval(row['genres'])
        da.tags['title'] = row['title']
        
        # da.tags['cast'] = ast.literal_eval(row['cast'])
        # da.tags['keywords'] = ast.literal_eval(row['keywords'])
        docs.append(da)

    # print(da.text)

    da.plot('document.svg')

# print(docs[0].json())
# for d in docs:
#     d.plot()

print(docs[0].granularity)
print(docs[0].adjacency)
print(type(docs.get_vocabulary()))
# docs.plot_image_sprites(output=None, canvas_size=512, min_size=16, channel_axis=- 1)
# docs.plot_embeddings(title='MyDocumentArray', image_sprites=False, min_image_size=16, channel_axis=- 1, start_server=True)

# da.plot()

# print(da[])
# print(da[2].tags)


# print(da[1].text)

if __name__ == "__main__":
    model = "sentence-transformers/paraphrase-distilroberta-base-v1"

    # flow = (
    #     Flow(install_requirements = True)
    #     .add(
    #         name="Text_Encoder",
    #         uses="jinahub://TransformerTorchEncoder",
    #         uses_with={"pretrained_model_name_or_path": model},
    #         install_requirements = True
    #     )
    #     .add(
    #         name="Text_Indexer",
    #         uses='jinahub://SimpleIndexer',
    #         uses_metas={'workspace': '/indexing/tmp_folder'},
    #         install_requirements = True
    #     )
    #     # .add(
    #     #     uses='jinahub+docker://CLIPTextEncoder/',
    #     #     install_requirements = True
    #     #     )
    # )

    # "en_core_web_md"
    flow = (
        Flow()
        # .add(
        #     uses="jinahub://SpacyTextEncoder",
        #     uses_with={"model_name": "en_core_web_md"},
        #     name="Spacy_encoder",
        #     install_requirements=True
        # )
        # .add(
        #     uses="jinahub+docker://SimpleIndexer",
        #     uses_metas={"workspace": "workspace/indexing"},
        #     volumes="./workspace:/workspace/workspace",
        #     name="Simple_indexer"
        # )
        .add(
        name='text_encoder',
        uses=TextEncoder,
        uses_with={'parameters': {'traversal_paths': 'r'}},       #changed c to r
        )
        .add(
            name='simple_indexer',
            uses=SimpleIndexer,
        )
    )   

    flow.plot('flow.svg')

    # with flow:
    #     flow.index(
    #         inputs=docs,
    #   )
    with flow:
        flow.post(on='/index', inputs=docs, on_done=print)
    

    # with flow:
    #     flow.index(
    #     inputs=docs,
    #     docs = docs
    #     # parameters = {'name' : 'something', 'xyz' : 'fsdfsdfsa'}
    # )

    query_flow = (
        Flow()
        # Create vector representations from query
        .add(name='query_transformer', uses=TextEncoder,)
        # Use encoded question to search our index
        .add(
            name='simple_indexer',
            uses=SimpleIndexer,
        )
    )


    query = Document(text = input('Query movie: '))
    with query_flow:
        # query = Document(text = input('Query movie : '))
        response = query_flow.post(on='/search', inputs = query, return_results = True)

    matches = response[0].docs[0].matches
    
    for ind, i in enumerate(matches):
        print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
        print()
        print(i.text)
        print()