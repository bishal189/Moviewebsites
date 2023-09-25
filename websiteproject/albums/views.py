from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums
from django.http import JsonResponse
# Create your views here.
from detailapp.models import Cartitem
def album(request):
    albums=Albums.objects.all()
    context={
        'albums':albums
    }
    return render(request,'album.html',context)


def album_detail(request,id):
    album=Albums.objects.get(id=id)
    movies=MovieDetail.objects.all()
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
        }
    else:
        context={
             'product':album,
            'movies':movies,
            

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
