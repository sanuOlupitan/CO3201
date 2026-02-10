import pandas as pd
from django.core.management.base import BaseCommand
from recommender.models import Movie

class Command(BaseCommand):
    #Imports Netflix data from CSV, cleans it, and prepares ML features

    def handle(self, *args, **kwargs):
        #loads the data
        self.stdout.write("Loading CSV file......")
        try:
            #makes sure netflix_titles.csv is in the main folder
            ##df = pd.read_csv('netflix_titles.csv', encoding='cp1252')#'latin-1' which handles special characters better than utf-8
            #iso-8859-1 to handle special characters
            df = pd.read_csv('netflix_titles.csv', encoding='iso-8859-1')

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found. Please make sure CSV file is in the root directory.'))
            return
        
        #this is the cleaning phase for the data
        self.stdout.write("Cleaning data...")

        #Handle Release Year specifically (It must be an Integer, not a String)
        #If the year is missing, we fill it with 0 so the database doesn't crash
        if 'release_year' in df.columns:
            df['release_year'] = df['release_year'].fillna(0).astype(int)


        #Replace NaN (Not a number) values with empty strings for the text columns
        df.fillna('')

        #Process and Save to database
        movies_to_create = []

        self.stdout.write("Processing Rows...")
        
        for index, row in df.iterrows():
            #this is where i construct the 'content soup' for the algorithm
            #it combines important text features into one big string
            soup = f"{row['title']} {row['director']} {row['cast']} {row['listed_in']} {row['description']}"

            #create the movie object
            movie = Movie(
                show_id=row['show_id'],
                type=row['type'],
                title=row['title'],
                director=row['director'],
                cast=row['cast'],
                country=row['country'],
                release_year=row['release_year'],
                rating=row['rating'],
                duration=row['duration'],
                listed_in=row['listed_in'],
                description=row['description'],
                content_soup=soup.lower() #lowercase helps search
            )
            movies_to_create.append(movie)

        #bulk create
        self.stdout.write(f"Importing {len(movies_to_create)} movies...")

        #clear existing data to avoid duplicates 
        Movie.objects.all().delete()

        Movie.objects.bulk_create(movies_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(movies_to_create)} items!'))