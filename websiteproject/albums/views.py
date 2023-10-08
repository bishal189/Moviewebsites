from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums,AlbumMovie,Separator
from django.http import JsonResponse
# Create your views here.
from django.core.paginator import Paginator
from django.core import serializers
from detailapp.models import Cartitem,Order_Product_album,Order_Product
def album(request):
    albums=Albums.objects.all()
    paginator_scene=Paginator(albums,10)
    page_scene=request.GET.get('albums')
    paged_scene=paginator_scene.get_page(page_scene)
    context={
        'albums':paged_scene
    }
    return render(request,'album.html',context)



def album_detail(request,id):
    album=Albums.objects.get(id=id)
    
    movies=MovieDetail.objects.filter(genre__in=album.genre.all(),type=album.type).order_by('-id').distinct()
    counter=0
    previous_movies_in_albums_bought=[]
    if request.user.is_authenticated:
        previous_album=Order_Product_album.objects.filter(user=request.user)
        for item in previous_album:
            previous_movies=item.product.movies.all()
            previous_movies_in_albums_bought.append(previous_movies)


    already_in_album=None
    if request.user.is_authenticated:
        globaldata,created=Separator.objects.get_or_create(user=request.user)
        albummovie,created=AlbumMovie.objects.get_or_create(user=request.user,album=album,separator=globaldata.separator)
        counter=albummovie.movies.count()
        already_in_album=albummovie.movies.all()

    count=movies.count()
    items_per_page = 20 # Adjust this to your preferred value

    # Create a Paginator object with the movies queryset
    paginator = Paginator(movies, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    movies = paginator.get_page(page_number)

    li=[]

    #type checker is used to check for scene in index page
    typeChecker=False
    if album.type=="Scene":
        typeChecker=True
    if request.user.is_authenticated:
        user=request.user
        cart_item=Cartitem.objects.filter(user=user)



        for item in cart_item:
                li.append(item.product)

        for item in previous_movies_in_albums_bought:
                for itemdata in item:
                    li.append(itemdata)
        previous_items=Order_Product.objects.filter(user=user)
    
        for item in previous_items:
            li.append(item.product)


        context={

            'product':album,
            'movies':movies,
            'already_in_album':already_in_album,
            'itemsincart':li,
            # 'counter':album.counter,
            'counter':counter,
            'all_products':movies,
            'typeChecker':typeChecker,
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
  globaldata=Separator.objects.get(user=request.user)  
  album_movie,created=AlbumMovie.objects.get_or_create(user=request.user,album=album,separator=globaldata.separator)
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
  globaldata=Separator.objects.get(user=request.user)
  album_movie=AlbumMovie.objects.get(user=request.user,album=album,separator=globaldata.separator)
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
    globaldata=Separator.objects.get(user=request.user)
    albummovie=AlbumMovie.objects.get(user=request.user,album=album,separator=globaldata.separator)

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