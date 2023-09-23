from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums
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
            'itemcount':len(li),
        }
    else:
        context={
             'product':album,
            'movies':movies,
            

        }
    return render(request,"album-detail.html",context)