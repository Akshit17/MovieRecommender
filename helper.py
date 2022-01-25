from collections import defaultdict
from jina import DocumentArray, DocumentArrayMemmap, Document
from jina import Executor, requests

import torch
from sentence_transformers import SentenceTransformer

class SimpleIndexer(Executor):
    """Simple indexer class"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self._docs = DocumentArrayMemmap(".")
        # self._docs = DocumentArrayMemmap()
        print("{} IS self.workspace".format(self.workspace))
        self._docs = DocumentArrayMemmap(self.workspace + '/indexer')

    @requests(on='/index')
    def index(self, docs: 'DocumentArray', **kwargs):
        # Stores the index in attribute
        if docs:
            self._docs.extend(docs)

    @requests(on='/search')
    def search(self, docs: 'DocumentArray', **kwargs):
        """Append best matches to each document in docs"""

        # Match query agains the index using cosine similarity
        docs.match(
            DocumentArray(self._docs),
            metric='cosine',
            normalization=(1, 0),
            limit=10,
            exclude_self=True,               #Seems to be not working as same matches found in 'match.svg' later
            # traversal_rdarray='r,',
            # traversal_rdarray='c,',         #says traversal_rdarray is deprecated
        )

        i = 1
        print(docs.embeddings.shape)
        for d in docs:
            if i == 1:
                d.plot('match1.svg')

            match_similarity = defaultdict(float)
            # For each match
            print("Type of d.matches is {} ".format(d.matches))
            for m in d.matches:
                # Get cosine similarity
                m.plot('m.svg')
                print("parent_id for m is {}".format(m.id))                  #giving an empty string for m.parent_id
                match_similarity[m.parent_id] += m.scores['cosine'].value

            sorted_similarities = sorted(
                match_similarity.items(), key=lambda v: v[1], reverse=True
            )

            print(match_similarity)
            print(sorted_similarities)

            # Rank matches by similarity and collect them

            # d.matches.clear()

            # for k, _ in sorted_similarities:
            #     m = Document(self._docs[k], copy=True)
            #     d.matches.append(m)
            #     # Only return top 10 answers
            #     if len(d.matches) >= 10:
            #         break

            # Remove embedding as it is not needed anymore
            d.pop('embedding')
        print(i)

class TextEncoder(Executor):
    def __init__(self, parameters: dict = {'traversal_paths': 'r'}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = SentenceTransformer(
            # 'multi-qa-MiniLM-L6-cos-v1', device='cuda', cache_folder='.'
            # 'multi-qa-MiniLM-L6-cos-v1', device='cpu', cache_folder='.'
            'all-MiniLM-L6-v2', device='cpu', cache_folder='.'
        )
        self.parameters = parameters
        # model = SentenceTransformer('')

    @requests(on=['/search', '/index'])
    def encode(self, docs: DocumentArray, **kwargs):
        """Wraps encoder from sentence-transformers package"""
        print("BEHOLD!!!! I AM EMBEDDING !!!!")
        traversal_paths = self.parameters.get('traversal_paths')
        target = docs.traverse_flat(traversal_paths)
        
        # count = 0
        # for i in target:
        #     count = count + 1             
        # print("elems in target are: {}".format(count))

        with torch.inference_mode():
            # print(target.texts)                           #gave none when travesal_path set to c
            embeddings = self.model.encode(target.texts)
            # print(embeddings.shape)             # gives (1 , 384) ??    now gives (100, 384)
            target.embeddings = embeddings