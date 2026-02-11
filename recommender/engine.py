import os
import pickle
from django.conf import settings
from sklearn.metrics.pairwise import linear_kernel

#global varibles
#now only load these once the server starts, not for every request

def load_model():
    path = os.path.join(settings.BASE_DIR, 'recommender/ml_models')
    try:
        #Loads the pre-calculated matrix and data
        with open(os.path.join(path, 'tfidf_matrix.pkl'), 'rb') as f:
            tfidf_matrix = pickle.load(f)
        with open(os.path.join(path, 'indices.pkl'), 'rb') as f:
            indices = pickle.load(f)
        with open(os.path.join(path, 'movie_data.pkl'), 'rb') as f:
            movie_data = pickle.load(f)
        return tfidf_matrix, indices, movie_data
    except FileNotFoundError:
        #if file doesnt exist yet, return none
        return None, None, None
    
#loads the models immediatey when django starts
tfidf_matrix, indices, movie_data = load_model()

def get_recommendations(title):
    #Safety Check: has model been trained?
    if tfidf_matrix is None or indices is None:
        return ["ERROR: Model not trained. Run 'python manage.py train_model' first."]
    
    #check if the movie exists inour database
    #use 'indices' to find matrix location 
    try:
        idx = indices[title]
    except KeyError:
        return [] #when movie not found
    
    #compute Similarity
    #only calculate the similarity for this specific move against the pre-calculated matrix
    cosine_sim = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix)

    #get top 10 scores
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    #Skip the searched movie in list
    sim_scores = sim_scores[1:11]

    #retrieve titles
    movie_indices = [i[0] for i in sim_scores]

    return movie_data['title'].iloc[movie_indices].tolist()

