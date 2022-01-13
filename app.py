import sys
import os
import ast
import csv
from jina import Document, DocumentArray, DocumentArrayMemmap
from jina import Flow, Executor


# da = DocumentArray.load_csv("./movies_metadata.csv")
#UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 455: character maps to <undefined>


# da = DocumentArray.load_csv("./movies_metadata.csv", encoding="utf8")
#gives error with encoding .  No attribute named 'encoding' either to specify encoding or to use utf8

docs = DocumentArray()

with open("movies_metadata.csv", encoding="utf-8") as file:
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

    # da.plot()

# print(docs[0].json())
# for d in docs:
#     d.plot()

print(type(docs.get_vocabulary()))
# docs.plot_image_sprites(output=None, canvas_size=512, min_size=16, channel_axis=- 1)
# docs.plot_embeddings(title='MyDocumentArray', image_sprites=False, min_image_size=16, channel_axis=- 1, start_server=True)

# da.plot()

# print(da[])
# print(da[2].tags)


# print(da[1].text)

if __name__ == "__main__":
    model = "sentence-transformers/paraphrase-distilroberta-base-v1"

    flow = (
        Flow(install_requirements = True)
        .add(
            name="Text_Encoder",
            uses="jinahub://TransformerTorchEncoder",
            uses_with={"pretrained_model_name_or_path": model},
            install_requirements = True
        )
        # .add(
        #     name="Text_Indexer",
        #     uses='jinahub://SimpleIndexer',
        #     uses_metas={'workspace': '/indexing/tmp_folder'},
        #     install_requirements = True
        # )
        .add(
            uses='jinahub+docker://CLIPTextEncoder/',
            install_requirements = True
            )
    )

    print(flow)

    # with flow:
    #     flow.index(
    #         inputs=docs,
    #   )

    with flow:
        flow.index(
        inputs=docs,
        docs = docs,
        parameters = {'name' : 'something', 'xyz' : 'fsdfsdfsa'}
    )

    query = Document(text = input('Query song : '))
    with flow:
        response = flow.search(inputs = query, return_results = True)

    matches = response[0].docs[0].matches
        
    for ind, i in enumerate(matches):
        print(f' Movie Title :  {i.tags["title"]} '.center(60,'='))
        print()
        print(i.text)
        print()