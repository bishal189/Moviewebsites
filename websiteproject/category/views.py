from django.shortcuts import render
from .models import Category
from indexapp.models import MovieDetail,StarsModel
# Create your views here.


def category(request):

     # category_count=Category.values.all().count()
     # print(category_count)
     genres=Category.objects.all()
     data=MovieDetail.objects.all()[:20]
     stardata=StarsModel.objects.all()
     context={
          'genres':genres,
          'data':data,
          'star':stardata,
     }
     return render(request,"category.html",context)

def category_filter(request):
    genres=Category.objects.all()
    genre=request.POST['genre']
    year=request.POST['year']
    age=request.POST['starage']
    hair=request.POST['starhaircolor']
    height=request.POST['starheight']
    price=request.POST['price']
    type=request.POST['type']
    star=None
    filters_movie={}
    filters_category={}
    filters_star={}
    current={
        'genre':None,
        'year':None,
        'age':None,
        'hair':None,
        'height':None,
        'price':None,
        'type':None,

    }
    if genre != "all":
        filters_category['category_name']=genre
        current['genre']=genre
    
    if year != "all":
        filters_movie['year']=year
        current['year']=year

    if age != "all":
        current['age']=age
        lower_bound, upper_bound = age.split('-')

        filters_star['age__range']=(float(lower_bound),float(upper_bound))

    if hair != "all":
        current['hair']=hair
        filters_star['haircolor']=hair

    if height != "all":
        current['height']=height
        lower_bound,upper_bound=height.split('-')
        filters_star['height__range']=(float(lower_bound),float(upper_bound))
        

    if price != "all":
        current['price']=price
        lower_bound,upper_bound=price.split('-')
        filters_movie['price__range']=(float(lower_bound),float(upper_bound))



    if type != "all":
        current['type']=type
        filters_movie['type']=type

    category=None
    if filters_category:
        category=Category.objects.get(**filters_category)
    if filters_star:
        star=StarsModel.objects.filter(**filters_star)


    if filters_star and filters_category and filters_movie:

        movies=MovieDetail.objects.filter(**filters_movie,genre=category,stars__in=star)
    
    elif filters_star and filters_movie:
        movies=MovieDetail.objects.filter(**filters_movie,stars__in=star)
    elif filters_category and filters_movie:
        movies=MovieDetail.objects.filter(**filters_movie,genre=category)
    elif filters_category and filters_star:
        movies=MovieDetail.objects.filter(stars__in=star,genre=category)


    elif filters_category:
        print(category)
        movies=MovieDetail.objects.filter(genre=category)
    elif filters_star:

        movies=MovieDetail.objects.filter(stars__in=star)
    elif filters_movie:
        movies=MovieDetail.objects.filter(**filters_movie)

    else:
        movies=MovieDetail.objects.all()





        

    stardata=StarsModel.objects.all()
    context={
          'genres':genres,
          'data':movies,
          'star':stardata,
          'current':current
     }
    return render(request,"category.html",context)

def category_by_genre(request,genrename):
     category=Category.objects.get(category_name=genrename)#first gets category
     genres=Category.objects.all()#get all genre to show as options
     datatoshow=MovieDetail.objects.all().filter(genre=category)[:20]#finally get movie based on category
     stardata=StarsModel.objects.all()

     context={
          'genres':genres,
          'data':datatoshow,
          'genre':genrename,
          'star':stardata,

     }


     return render(request,"category.html",context)

def category_by_year(request,year):
    genres=Category.objects.all()
    datatoshow=None
    stardata=StarsModel.objects.all()
    if year == 2016:
        datatoshow=MovieDetail.objects.all().filter(year__lt=year)[:20]
    else:
        datatoshow=MovieDetail.objects.all().filter(year=year)[:20]
    context={
        'year':year,
        'data':datatoshow,
        'genres':genres,
        'star':stardata,

    }
    return render(request,"category.html",context)

def combined_year_genre(request,year,genrename):

    category=Category.objects.get(category_name=genrename)#first gets category
    genres=Category.objects.all()
    datatoshow=None

    stardata=StarsModel.objects.all()

    if year==2016:
        datatoshow=MovieDetail.objects.all().filter(year__lt=year,genre=category)
    else:
        datatoshow=MovieDetail.objects.all().filter(year=year,genre=category)

    context={
        'genres':genres,
        'data':datatoshow,
        'genre':genrename,
        'year':year,
        'star':stardata,

    }
    return render(request,"category.html",context)

