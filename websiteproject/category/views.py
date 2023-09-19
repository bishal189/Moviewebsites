from django.shortcuts import render
from .models import Category
from indexapp.models import MovieDetail

# Create your views here.


def category(request):

     # category_count=Category.values.all().count()
     # print(category_count)
     genres=Category.objects.all()
     data=MovieDetail.objects.all()[:20]
     context={
          'genres':genres,
          'data':data,
     }
     return render(request,"category.html",context)


def category_by_genre(request,genrename):
     category=Category.objects.get(category_name=genrename)#first gets category
     genres=Category.objects.all()#get all genre to show as options
     datatoshow=MovieDetail.objects.all().filter(genre=category)[:20]#finally get movie based on category
     context={
          'genres':genres,
          'data':datatoshow,
          'genre':genrename,
     }


     return render(request,"category.html",context)

