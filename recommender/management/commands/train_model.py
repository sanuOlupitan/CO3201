import pandas as pd
import pickle
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from recommender.models import Movie

class Command(BaseCommand):
    #this computes the TF-IDF matrix and save it to the disk. this is for model persistence.

    def handle(self, *args, **kwargs):
        #fetch data
        self.stdout.write("fetching movies from database...")
        movies = Movie.objects.all().values('id', 'title', 'content_soup')
        df = pd.DataFrame(list(movies))

        if df.empty:
            self.stdout.write(self.style.ERROR("No movies found! Run import_netflix first."))
            return
        
        #compute TF-IDF matrix
        self.stdout.write("Training TF-IDF Model...")
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(df['content_soup'])

        #create mapping
        #to look up which row belongs to which movie
        indices = pd.Series(df.index, index=df['title']).drop_duplicates()

        #persistence
        #define the path to recommender/ml_models/
        model_path = os.path.join(settings.BASE_DIR, 'recommender/ml_models')

        #ensures dictionary exists
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        self.stdout.write(f"Saving models to {model_path}.....")

        #save to matrix
        with open(os.path.join(model_path, 'tfidf_matrix.pkl'), 'wb') as f:
            pickle.dump(tfidf_matrix, f)

        #Save the Indices
        with open(os.path.join(model_path, 'indices.pkl'), 'wb') as f:
            pickle.dump(indices, f)

        #Save the Dataframe 
        #faster than querying DB again
        with open(os.path.join(model_path, 'movie_data.pkl'), 'wb') as f:
            pickle.dump(df, f)

        self.stdout.write(self.style.SUCCESS("Successfully trained and saved the model!"))