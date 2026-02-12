from django.shortcuts import render
from .models import Movie
from .engine import get_recommendations

def index(request):
    recommendations = []
    search_query = request.GET.get('q') #get the text from the search box

    if search_query:
        #get the list of the titles from the ML engine
        rec_titles = get_recommendations(search_query)

        #if we get the desired result, fetch the acual movie object from the db
        if rec_titles:
            #fetch all recommended movies
            rec_movies = Movie.objects.filter(title__in=rec_titles)

            #preserve the ranking order
            #created a dictionary to look up movies by title
            rec_dict = {movie.title: movie for movie in rec_movies}

            #this rebuilds the list in the exact order the ML Engine predicted
            recommendations = [rec_dict[title] for title in rec_titles if title in rec_dict]

    return render(request, 'recommender/index.html', {
        'recommendations': recommendations,
        'search_query': search_query
    })
