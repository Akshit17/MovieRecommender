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
        self._docs = DocumentArrayMemmap()

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
            limit=100,
            exclude_self=True,               #added Manually 
            traversal_rdarray='r,',
            # traversal_rdarray='c,',         #says traversal_rdarray is deprecated
        )

        i = 1
        print(docs.embeddings.shape)
        for d in docs:
            i += 1
            d.plot('match.svg')
            match_similarity = defaultdict(float)
            # For each match
            for m in d.matches:
                # Get cosine similarity
                match_similarity[m.parent_id] += m.scores['cosine'].value

            sorted_similarities = sorted(
                match_similarity.items(), key=lambda v: v[1], reverse=True
            )

            print(match_similarity)

            # Rank matches by similarity and collect them
            d.matches.clear()
            for k, _ in sorted_similarities:
                m = Document(self._docs[k], copy=True)
                d.matches.append(m)
                # Only return top 10 answers
                if len(d.matches) >= 10:
                    break
            # Remove embedding as it is not needed anymore
            d.pop('embedding')
        print(i)

class TextEncoder(Executor):
    def __init__(self, parameters: dict = {'traversal_paths': 'r'}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = SentenceTransformer(
            # 'multi-qa-MiniLM-L6-cos-v1', device='cuda', cache_folder='.'
            'multi-qa-MiniLM-L6-cos-v1', device='cpu', cache_folder='.'
        )
        self.parameters = parameters
        model = SentenceTransformer('')

    @requests(on=['/search', '/index'])
    def encode(self, docs: DocumentArray, **kwargs):
        """Wraps encoder from sentence-transformers package"""
        traversal_paths = self.parameters.get('traversal_paths')
        target = docs.traverse_flat(traversal_paths)
        
        count = 0
        for i in target:
            count = count + 1
        print("elems in target are: {}".format(count))
        with torch.inference_mode():
            embeddings = self.model.encode(target.texts)
            print(embeddings.shape)             # gives (1 , 384) ??
            target.embeddings = embeddings