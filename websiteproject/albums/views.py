from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums
from django.http import JsonResponse
# Create your views here.
from django.core.paginator import Paginator

from detailapp.models import Cartitem
def album(request):
    albums=Albums.objects.all()
    context={
        'albums':albums
    }
    return render(request,'album.html',context)


def album_detail(request,id):
    album=Albums.objects.get(id=id)
    movies=MovieDetail.objects.filter(genre__in=album.genre.all())
    count=movies.count()
    items_per_page = 5 # Adjust this to your preferred value

    # Create a Paginator object with the movies queryset
    paginator = Paginator(movies, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    movies = paginator.get_page(page_number)

    li=[]
    user=request.user
    if request.user.is_authenticated:

        cart_item=Cartitem.objects.filter(user=user)

        for item in cart_item:
                li.append(item.product)
    
        

        context={
            'product':album,
            'movies':movies,
            'itemsincart':li,
            'counter':album.counter,
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

  album.movies.add(movie)
  album.counter=album.movies.count()
  album.save()
  data = {
        'status': 'success',
        'count':album.counter,
    }
  return JsonResponse(data)

def dec_counter(request,album_id,movie_id):
  album=Albums.objects.get(id=album_id)
  movie=MovieDetail.objects.get(id=movie_id)

  album.movies.remove(movie)

  album.counter=album.movies.count()
  if album.counter<0:
    album.counter=0
  
  album.save()
  data = {
        'status': 'success'
    }
  return JsonResponse(data)
