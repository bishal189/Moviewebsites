from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums,AlbumMovie
from django.http import JsonResponse
# Create your views here.
from django.core.paginator import Paginator
from django.core import serializers
from detailapp.models import Cartitem,Order_Product_album
def album(request):
    albums=Albums.objects.all()
    context={
        'albums':albums
    }
    return render(request,'album.html',context)


def album_detail(request,id):
    album=Albums.objects.get(id=id)
    movies=MovieDetail.objects.filter(genre__in=album.genre.all()).order_by('-id')
    counter=0
    already_in_album=None
    if request.user.is_authenticated:
         albummovie=AlbumMovie.objects.get(user=request.user,album=album)
         counter=albummovie.movies.count()
         already_in_album=albummovie.movies.all()


    count=movies.count()
    items_per_page = 10 # Adjust this to your preferred value

    # Create a Paginator object with the movies queryset
    paginator = Paginator(movies, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    movies = paginator.get_page(page_number)
    albums_bought=[]
    if request.user.is_authenticated:
        album_bought=Order_Product_album.objects.filter(user=request.user)
        for item in album_bought:
            albums_bought.append(item.product.album.id)

    li=[]
    if request.user.is_authenticated:
        user=request.user


        cart_item=Cartitem.objects.filter(user=user)

        for item in cart_item:
                li.append(item.product)

   
    
        print(albums_bought)

        context={
            'albums_bought':albums_bought,
            'product':album,
            'movies':movies,
            'already_in_album':already_in_album,
            'itemsincart':li,
            # 'counter':album.counter,
            'counter':counter,
            'all_products':movies,
            'count':count
        }
    else:
        context={
             'product':album,
            'movies':movies,
            'all_products':movies,
            'count':count
            

        }
    return render(request,"album-detail.html",context)

def inc_counter(request,album_id,movie_id):
  album=Albums.objects.get(id=album_id)
  movie=MovieDetail.objects.get(id=movie_id)  
  album_movie,created=AlbumMovie.objects.get_or_create(user=request.user,album=album)
  album_movie.movies.add(movie)
  album_movie.counter=album_movie.movies.count()
  album_movie.save()
  data = {
        'status': 'success',
        'count':album_movie.counter,
    }
  return JsonResponse(data)

def dec_counter(request,album_id,movie_id):
  album=Albums.objects.get(id=album_id)
  movie=MovieDetail.objects.get(id=movie_id)
  album_movie=AlbumMovie.objects.get(user=request.user,album=album)
  album_movie.movies.remove(movie)

  album_movie.counter=album.movies.count()
  if album_movie.counter<0:
    album.counter=0
  
  album_movie.save()
  data = {
        'status': 'success'
    }
  return JsonResponse(data)
def get_movies_in_album(request,album_id):
    album=Albums.objects.get(id=album_id)
    print(album)
    albummovie=AlbumMovie.objects.get(user=request.user,album=album)
    print(albummovie.movies.all())

    movie_data_list = []

    # Iterate through the movies and construct the full image URL for each
    for movie in albummovie.movies.all():
        if movie.coverphoto:
            coverphoto_url = request.build_absolute_uri(movie.coverphoto.url)
        else:
            coverphoto_url = None

        movie_data = {
            'movie_name': movie.movie_name,
            'coverphoto': coverphoto_url,
            # Add other movie data as needed
        }

        # Append the movie data to the list
        movie_data_list.append(movie_data)




    return JsonResponse({'status':"true","movies":movie_data_list})