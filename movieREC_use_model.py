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

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]         # remove movies with <10 ratings
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]     # remove user data from the dataset if they've voted less than 50 times

csr_data = csr_matrix(final_dataset.values)  # perform our conversion for a csr_matrix
final_dataset.reset_index(inplace=True)      # this way we don't have all the original indexes, we accordian it down

knn = pickle.load(open('knnpickle_file', 'rb'))

# this is our recommendation function
    # user inputs a movie name, and we'll spit out the 10 closest movies
def get_movie_recommendation(movie_name):   
    n_movies_to_recommend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx = movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx], n_neighbors = n_movies_to_recommend + 1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0]})
        df = pd.DataFrame(recommend_frame, index=range(1,n_movies_to_recommend+1))
        return df
    else:
        return "No movies found. Please check your input"

df = get_movie_recommendation('Iron Man')
#print(df)


def rec_10():
    user_movie = input("Please enter a movie title: ")
    if user_movie:
        df = get_movie_recommendation(str(user_movie))
        print(df)
    else:
        exit()

for i in range(2):
    rec_10()
