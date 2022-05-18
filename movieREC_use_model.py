import re
import pandas as pd
import numpy as np
import pickle
from scipy.sparse import csr_matrix

movies = pd.read_csv("movies.csv")       # import datasets for movies and their ratings
ratings = pd.read_csv("ratings.csv")

final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')    # rows are movieIDs, columns are userIDs
final_dataset.fillna(0, inplace=True)   # anything that was NaN (not a number) b4 is now a 0

no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 1].index,:]         # remove movies with <10 ratings
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 1].index]     # remove user data from the dataset if they've voted less than 50 times

csr_data = csr_matrix(final_dataset.values)  # perform our conversion for a csr_matrix
final_dataset.reset_index(inplace=True)      # this way we don't have all the original indexes, we accordian it down

knn = pickle.load(open('knnpickle_file', 'rb'))


# this is our recommendation function
    # user inputs a movie name, and we'll spit out the 10 closest movies
def get_movie_recommendation(movie_name):
    n_movies_to_recommend = 15
    movie_list = movies[movies['title'].str.contains(movie_name)]        # once we hash a movie name to an index, the index could be out of bounds
    
    found_movie = movie_list.iloc[0]['title']
    #print(found_movie)

    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]

        distances, indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_recommend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        
        recommend_frame = []
        
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_recommend+1))
        return df, found_movie
    
    else:
        
        return "No movies found. Please check your input", None



def rec_10(user_movie):
    user_movie = user_movie.lower()               # make everything lowercase, then capitalize each word
    user_movie = user_movie.title()
    try:
        df, found_movie = get_movie_recommendation(user_movie)
        return df, found_movie
    except IndexError:        # we get this a lot, especially when entering 'garfield' or 'comedy'
        # please try another movie
        print("Sorry")

def titles_only(txt):
    titles = re.findall('\d+\s+(.+)\s+\(\d{4}\)\s+[\.\d]+\n', txt)           # \d is a digit, . means any char, + is 1 or more times, {4} means 4 times (for the year), [] means can be any of the characters inside the [], + to say 1 or more times again
    return titles       # returns a list of movie names bc of the (.+), note: \s+ is any amt of whitespace

if __name__ == '__main__':
    user_movie = input("Please enter a movie title: ")
    ten_rec, found_movie = rec_10(user_movie)
    recommendations = titles_only(str(ten_rec))
    print("Found movie: ", found_movie)
    print('\n'.join(recommendations))


"""
    -- IMDB api that returns a picture of the movie
    -- and get 
"""