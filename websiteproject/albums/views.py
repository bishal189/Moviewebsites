from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums
# Create your views here.

def album(request):
    albums=Albums.objects.all()
    context={
        'albums':albums
    }
    return render(request,'album.html',context)

def album_detail(request,id):
    album=Albums.objects.get(id=id)
    context={
        'product':album,
    }
    return render(request,"album-detail.html",context)