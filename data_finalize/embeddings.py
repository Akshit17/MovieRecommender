from sentence_transformers import SentenceTransformer
import pickle
import logging
import multiprocessing
import pandas as pd


logging.basicConfig(format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)#, handlers=[LoggingHandler()])

def main():
    model = SentenceTransformer('all-MiniLM-L12-v2')
    sentences = []

    movies_metadata = pd.read_csv("./data_finalize/movies_metadata.csv")
    for i in movies_metadata['tags']:
        sentences.append(i)

    #Start the multi-process pool on all available CUDA devices
    pool = model.start_multi_process_pool()

    embeddings = model.encode_multi_process(sentences, pool)

    #Store sentences & embeddings on disc
    with open('embeddings.pkl', "wb") as fOut:
        pickle.dump({'sentences': sentences, 'embeddings': embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    multiprocessing.freeze_support()
    # main()

#Load sentences & embeddings from disc
with open('./data_finalize/embeddings.pkl', "rb") as fIn:
    stored_data = pickle.load(fIn)
    stored_sentences = stored_data['sentences']
    stored_embeddings = stored_data['embeddings']
    
    print(stored_sentences[0])
    print(type(stored_embeddings[0]))
    print(stored_embeddings[0])

