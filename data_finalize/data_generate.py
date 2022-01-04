import imdb
# from numba.core import target_extension
import pandas as pd
import numpy as np
import ast
# from numba import jit, cuda
import multiprocessing 


# import dask.dataframe as ddf
# import code
# code.interact(local=locals)

# https://stackoverflow.com/questions/54934012/getting-10-000-movie-plots-with-imdbpy      
# Press F to pay respect 

# moviesDB = imdb.IMDb()

# print(dir(moviesDB))       #prints all the functions/methods in this lib

# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', 
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', 
# '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_defModFunct', 
# '_getRefs', '_get_infoset', '_get_keyword', '_get_list_content', '_get_movie_list', '_get_real_characterID', 
# '_get_real_companyID', '_get_real_movieID', '_get_real_personID', '_get_search_content', '_get_search_movie_advanced_content', 
# '_get_top_bottom_movies', '_http_logger', '_keywordsResults', '_mdparse', '_normalize_characterID', '_normalize_companyID', 
# '_normalize_movieID', '_normalize_personID', '_purge_seasons_data', '_reraise_exceptions', '_results', '_retrieve', 
# '_searchIMDb', '_search_character', '_search_company', '_search_episode', '_search_keyword', '_search_movie', 
# '_search_movie_advanced', '_search_person', 'accessSystem', 'character2imdbID', 'compProxy', 'company2imdbID', 
# 'del_cookies', 'do_adult_search', 'get_bottom100_movies', 'get_character', 'get_character_infoset', 'get_company', 
# 'get_company_infoset', 'get_company_main', 'get_episode', 'get_imdbCharacterID', 'get_imdbCompanyID', 'get_imdbID', 
# 'get_imdbMovieID', 'get_imdbPersonID', 'get_imdbURL', 'get_keyword', 'get_movie', 'get_movie_airing', 'get_movie_akas', 
# 'get_movie_alternate_versions', 'get_movie_awards', 'get_movie_connections', 'get_movie_crazy_credits', 'get_movie_critic_reviews', 
# 'get_movie_episodes', 'get_movie_external_reviews', 'get_movie_external_sites', 'get_movie_faqs', 'get_movie_full_credits', 
# 'get_movie_goofs', 'get_movie_infoset', 'get_movie_keywords', 'get_movie_list', 'get_movie_locations', 'get_movie_main', 
# 'get_movie_misc_sites', 'get_movie_news', 'get_movie_official_sites', 'get_movie_parents_guide', 'get_movie_photo_sites', 
# 'get_movie_plot', 'get_movie_quotes', 'get_movie_recommendations', 'get_movie_release_dates', 'get_movie_release_info', 
# 'get_movie_reviews', 'get_movie_sound_clips', 'get_movie_soundtrack', 'get_movie_synopsis', 'get_movie_taglines', 
# 'get_movie_technical', 'get_movie_trivia', 'get_movie_tv_schedule', 'get_movie_video_clips', 'get_movie_vote_details', 
# 'get_person', 'get_person_awards', 'get_person_biography', 'get_person_filmography', 'get_person_genres_links', 
# 'get_person_infoset', 'get_person_keywords_links', 'get_person_main', 'get_person_news', 'get_person_official_sites', 
# 'get_person_other_works', 'get_person_publicity', 'get_popular100_movies', 'get_popular100_tv', 'get_proxy', 
# 'get_special_methods', 'get_top250_indian_movies', 'get_top250_movies', 'get_top250_tv', 'listProxy', 'mProxy', 
# 'name2imdbID', 'new_character', 'new_company', 'new_movie', 'new_person', 'pProxy', 'scompProxy', 'search_character', 
# 'search_company', 'search_episode', 'search_keyword', 'search_movie', 'search_movie_advanced', 'search_person', 'set_cookies',
#  'set_imdb_urls', 'set_proxy', 'set_timeout', 'skProxy', 'smProxy', 'smaProxy', 'spProxy', 'title2imdbID', 'topBottomProxy',
#  'update', 'update_series_seasons', 'urlOpener', 'urls']

# ml_25_movies= pd.read_csv("generated_ml_25_movies.csv")
# # ml_25_movies = pd.read_csv("ml_25_movies.csv")
# # ml_25_movies["overview"] =  np.nan  
# # print(type(ml_25_movies['cast'][35000]))
# # ml_25_movies["cast"] =  np.nan  
# ml_25_movies["keywords"] =  np.nan  


# # create as many processes as there are CPUs on your machine
# num_processes = multiprocessing.cpu_count()
# # create our pool with `num_processes` processes
# pool = multiprocessing.Pool(processes=num_processes)


# # calculate the chunk size as an integer
# chunk_size = int(ml_25_movies.shape[0]/num_processes)

# # this solution was reworked from the above link.
# # will work even if the length of the dataframe is not evenly divisible by num_processes
# chunks = [ml_25_movies.loc[ml_25_movies.index[i:i + chunk_size]] for i in range(0, ml_25_movies.shape[0], chunk_size)]


# print(ml_25_movies.head(10))

'''mobiee = moviesDB.search_movie('Toy Story (1995)')
print(mobiee[0].getID())
for mobie in mobiee:
    # print(type(mobie))
    print(mobie.keys)
    print(mobie['title'])
    print(mobie['year'])'''

# print(ml_25_movies['imdb_id'][0])
    
# overview = []
# id_list = ml_25_movies['imdb_id'].to_list()
# title_list = ml_25_movies['title'].to_list()

# for i in range(0 , 5):                   #if length of imdb_id is less than 7 then add zeroes in prefloc
#     id = str(ml_25_movies['imdb_id'][i])
# for index , id in enumerate(ml_25_movies["imdb_id"].iteritems()):
#     # print(index)

# @cuda.jit(target='cuda')
def gen_shi(ml_25_movies):
    print(type(ml_25_movies))
    for index , id in ml_25_movies.iterrows():
        if(type(ml_25_movies["cast"][index]) == float):
            # print(id)
            id = str(id['imdb_id'])
            if len(id) < 7:
                id = '0' + id
            movie = moviesDB.get_movie(id)
            # print(type(movie))
            # print(movie.keys())                      #gives attributes that can be used
            # print(movie['cast'])                      # ['rating'] year and title too 
            # print(movie['directors'])
            #print(movie)                              #ends weirdly with  '::<something@gmail.com>' or '::somename'
            # print(movie['plot outline'])

            # try: 
            #     # print(index)
            #     overview.append(movie['plot'])                  #gives error for some movies
            # except:
            #     print(index)
            #     print(ml_25_movies['title'][index])        
            try:
                # print(movie['plot'])
                print("added plo/cas")
                ml_25_movies.iat[index, 5] = movie['plot']
                ml_25_movies.iat[index, 6] = movie['cast']
            except:
                # print(id)
                ml_25_movies.drop(index)
                # ml_25_movies.drop(index, inplace=True)

            movie = moviesDB.get_movie(id, info=['keywords'])
            try:
                print("added keybord")
                # print(movie['keywords'])
                ml_25_movies.iat[index, 7] = movie['keywords']
            except:
                # print(id)
                ml_25_movies.drop(index)
                # ml_25_movies.drop(index, inplace=True)

            
            # if index % 1000 == 0:
            #     print(id)
            #     print("One batch Komplet") 

            # # ml_25_movies["overview"] = pd.Series(overview)     #adding overview column to dataframe
            # # ml_25_movies.to_csv('generated_ml_25_movies.csv', index = False)

            # ml_25_movies.to_csv('dask_generated_ml_25_movies.csv', index = False)

            # print(ml_25_movies)
    print(ml_25_movies)
    return ml_25_movies

def main():
     # apply our function to each chunk in the list
    result = pool.map(gen_shi, chunks)

    # for i in range(len(result)):
    #     # since result[i] is just a dataframe
    #     # we can reassign the original dataframe based on the index of each chunk
    #     ml_25_movies.loc[result[i].index] = result[i]
    ml_25_movies = pd.concat(result)
    # print(result)

    ml_25_movies.to_csv('mp_generated_ml_25_movies.csv', index = False)
    # print(ml_25_movies)


    pool.close()
    pool.join()

moviesDB = imdb.IMDb()
if __name__ == '__main__': 
    multiprocessing.freeze_support()
    
    # moviesDB = imdb.IMDb()
    # ml_25_movies= pd.read_csv("generated_ml_25_movies.csv")
    ml_25_movies= pd.read_csv("mp_generated_ml_25_movies.csv")
    # ml_25_movies["overview"] =  np.nan 
    # ml_25_movies["cast"] =  np.nan 
    # ml_25_movies["keywords"] =  np.nan  
    print(type(ml_25_movies['overview'][1]))
    print(type(ml_25_movies['cast'][1]))
    print(type(ml_25_movies['keywords'][1]))

    # create as many processes as there are CPUs on your machine
    num_processes = multiprocessing.cpu_count() - 1
    # create our pool with `num_processes` processes
    pool = multiprocessing.Pool(processes=num_processes)

    # calculate the chunk size as an integer
    chunk_size = int(ml_25_movies.shape[0]/num_processes)

    # this solution was reworked from the above link.
    # will work even if the length of the dataframe is not evenly divisible by num_processes
    chunks = [ml_25_movies.loc[ml_25_movies.index[i:i + chunk_size]] for i in range(0, ml_25_movies.shape[0], chunk_size)]
    # print(chunks)


    main()

#     # gen_shi(moviesDB, ml_25_movies)

#     # df_dask = ddf.from_pandas(ml_25_movies, npartitions=6)
#     # new_df = df_dask.map_partitions(gen_shi, moviesDB).compute(scheduler='processes')


# print(moviesDB.get_movie_infoset())

# movie = moviesDB.get_movie("0113497", info=['plot', 'cast', 'keywords'])
# movie = moviesDB.get_movie("0114709")
# print(movie.items())
# print(movie.get('keywords'))
# print(movie.infoset2keys)

# print(movie['keywords'])
# cast = movie.get('cast')

# actor = movie['cast'][0]
# print(actor)
# print(actor.currentRole)

# movie = moviesDB.get_movie("0114709", info=['plot'])
# print(movie['keywords'])
# print(movie['plot'])

# print(ml_25_movies.head(10))


# ['localized title', 'cast', 'genres', 'runtimes', 'countries', 'country codes', 'language codes', 'color info', 'aspect ratio',
#  'sound mloc', 'box office', 'certificates', 'original air date', 'rating', 'votes', 'cover url', 'imdbID', 
# 'plot outline',
#  'languages', 'title', 'year', 'kind', 'directors', 'writers', 'producers', 'composers', 'cinematographers', 'editors', 
# 'editorial department', 'casting directors', 'production designers', 'art directors', 'set decorators', 'costume designers', 'make up department', 
# 'production managers', 'assistant directors', 'art department', 'sound department', 'special effects', 'visual effects', 
# 'stunts', 'camera department', 'casting department', 'costume departmen', 'location management', 'music department', 
# 'script department', 'transportation 
#department', 'miscellaneous', 'thanks', 'akas', 'writer', 'director', 'production companies',
#  'distributors', 'special effects companies', 'other companies', 
# 'plot', 'synopsis', 'canonical title', 
# 'long imdb title', 'long imdb canonical title', 'smart canonical title', 'smart long imdb canonical title', 
# 'full-size cover url']
 

# for movie in ml_25_movies['title']:
#     movies = moviesDB.search_movie(movie)
#     for val in movies:
#         print(val)