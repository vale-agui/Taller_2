from django.shortcuts import render
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64
from .models import Movie

# create your views here

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    matplotlib.use('Agg')

    # Obtener todas las películas
    all_movies = Movie.objects.all()

    # ---- Gráfica de cantidad de películas por año ----
    movie_counts_by_year = {}

    for movie in all_movies:
        year = movie.year if movie.year else "None"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    bar_positions_years = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions_years, movie_counts_by_year.values(), width=0.5, align='center')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_years, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_years = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # ---- Gráfica de cantidad de películas por género ----
    movie_counts_by_genre = {}

    for movie in all_movies:
        genres = movie.genre.split(',') if movie.genre else []
        if genres:
            first_genre = genres[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    bar_positions_genres = range(len(movie_counts_by_genre))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions_genres, movie_counts_by_genre.values(), width=0.5, align='center', color='skyblue')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions_genres, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_genres = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    return render(request, 'statistics.html', {
        'graphic_years': graphic_years,
        'graphic_genres': graphic_genres
    })
