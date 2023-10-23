from django.shortcuts import render
from django.http import HttpResponse
from movies.models import Movie, Person, MovieCredit
# Create your views here.


def index(request):
    movies = Movie.objects.all()
    context = {'movie_list': movies}
    return render(request, "movies/index.html", context=context)


def movie_detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    credits = MovieCredit.objects.filter(movie=movie.id)
    context = {'movie': movie, 'credits': credits}
    return render(request, "movies/movie_detail.html", context=context)
