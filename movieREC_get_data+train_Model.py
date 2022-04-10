import pandas as pd
import numpy as np
import pickle
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
movies = pd.read_csv("movies.csv")       # import datasets for movies and their ratings
ratings = pd.read_csv("ratings.csv")

#movies.head()     # show 1st five movies (we have movie-ID, title, and genre)
#ratings.head()    # show 1st five ratings (we have userID, movieID, rating and timestamp)

final_dataset = ratings.pivot(index='movieId', columns='userId', values='rating')    # rows are movieIDs, columns are userIDs
#final_dataset.head()

final_dataset.fillna(0, inplace=True)   # anything that was NaN (not a number) b4 is now a 0
#final_dataset.head()

no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')

# below, we use matplotlib to visualize our data 
    # any dots below the line y=10 are to be removed because not enough people gave it a rating
f, ax = plt.subplots(1, 1, figsize = (16, 4))
# ratings['rating'].plot(kind='hist')
plt.scatter(no_user_voted.index, no_user_voted, color='mediumseagreen')
plt.axhline(y = 10, color='r')
plt.xlabel('MovieId')
plt.ylabel('No. of users voted')
#plt.show()

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]         # remove movies with <10 ratings
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]     # remove user data from the dataset if they've voted less than 50 times
#final_dataset

# a lot of values in our final dataset (dim of 2121 * 378) are sparse (value of 0)
    # use csr_matrix from the scipy library
"""
how to use csr_matrix:
sample = np.array([[0,0,3,0,0],[4,0,0,0,2],[0,0,0,0,1]])
sparsity = 1.0 - ( np.count_nonzero(sample) / float(sample.size) )
print(sparsity)                       # is around 73%
csr_sample = csr_matrix(sample)       # perform the conversion
print(csr_sample)
"""
csr_data = csr_matrix(final_dataset.values)  # perform our conversion for a csr_matrix
final_dataset.reset_index(inplace=True)      # this way we don't have all the original indexes, we accordian it down

# now we'll use the KNN algorithm
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)     # these metrics were outlined in our tutorial. Using the cosine dist metrix is much more efficient than the pearson coefficient
knn.fit(csr_data)                           # train our model
knnPickle = open('knnpickle_file', 'wb')    # binary file to store our trained model
pickle.dump(knn, knnPickle)                 # use pickle library dump() func to store our knn model (process is specific to knn, not python)

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
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame, index=range(1,n_movies_to_recommend+1))
        return df
    else:
        return "No movies found. Please check your input"

