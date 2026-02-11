import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import Movie

def get_recommendations(titles):
    #fetches all movies from database
    #uses .values() to get a list of dictionaries
    movies = Movie.objects.all().values('title', 'content_soup')

    #converts into dataframe
    df = pd.DataFrame(movies)

    #validation 
    #checks if the movie exist
    if titles not in df['title'].values:
        return []
    
    #TF-IDF Vectorization
    #converts the "content Soup" text in a matrix of numbers
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content_soup'])

    #computing cosine similarity
    #calculates the similarity score between the target movie and all others
    #finds the index of the movie the user searched for 
    idx = df.index[df['title'] == title][0]

    #calculate similarity scores
    cosine_sim = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix)

    #get top 10 rec
    #flatten matrix results to 1d array
    sim_scores = list(enumerate(cosine_sim[0]))

    #sort movies based on the similarity scores with the highest first
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #gets the scores with the 10 most similar movies, whilst ignoring the first one which is itselfs
    sim_scores = sim_scores[1:11]

    #movie indices
    movie_indices = [i[0] for i in sim_scores]

    #return the titles to the recommended movies
    return df['title'].iloc[movie_indices].tolist()