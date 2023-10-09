from django.shortcuts import render
from .models import Category
from indexapp.models import MovieDetail,StarsModel,FavouritesModel
from detailapp.models import Cartitem
from django.db.models import  Sum
from django.contrib.auth.models import AnonymousUser


#Request to category page can be removed now as no category page is available now 
def category(request):
     genres=Category.objects.all()
     data=MovieDetail.objects.all()[:20]
     stardata=StarsModel.objects.all()
     haircolor=StarsModel.objects.values('haircolor').distinct()

     context={
          'genres':genres,
          'data':data,
          'star':stardata,
          'haircolor':haircolor,
     }

     return render(request,"category.html",context)
    

#filtering mechanism which filters based on post data from index page
def category_filter(request):
    genres=Category.objects.all()

    ###Get all data from post
    genre=request.POST['genre']
    year=request.POST['year']
    age=request.POST['starage']
    hair=request.POST['starhaircolor']
    height=request.POST['starheight']
    price=request.POST['price']
    type=request.POST['type']
    popularity=request.POST['popularity']
    ####

    ###To deterrmine which filters are applied
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
        'popularity':None,

    }
    if genre != "all":
        filters_category['category_name']=genre
        current['genre']=genre
    
    if year != "all":
        filters_movie['year']=year
        current['year']=year
    
    if popularity!="all":
        current['popularity']=popularity

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
    star=None
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
        movies=MovieDetail.objects.filter(genre=category)
    elif filters_star:

        movies=MovieDetail.objects.filter(stars__in=star)
    elif filters_movie:
        movies=MovieDetail.objects.filter(**filters_movie)

    else:
        movies=MovieDetail.objects.all().order_by('-id')
    
    # now getting data based on type
    get_dvd=movies.filter(type="DVD")
    get_scene=movies.filter(type="Scene")
    get_photoset=movies.filter(type="PhotoSets")

    stardata=StarsModel.objects.all()
    haircolor=StarsModel.objects.values('haircolor').distinct()
    
    if popularity == "Videos":
        movies=movies.order_by('-view_count','-cart_count','-id')
    
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):# same as request.user.is_authenticated
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)


    if popularity=="Genres":
        categories_with_counts = Category.objects.annotate(
        total_view_count=Sum('moviedetail__view_count'),
        total_cart_count=Sum('moviedetail__cart_count')
        )
        sorted_categories = categories_with_counts.order_by('-total_view_count', '-total_cart_count')

    
# Order the categories by total_view_count and total_cart_count
        context={
          'genres':genres,
          'sort_category':True,
          'categories':sorted_categories,
          'data_dvd':get_dvd,
          'data_scene':get_scene,
          'data_photoset':get_photoset,
          'star':stardata,
          'current':current,
          'haircolor':haircolor,
          'user_favourite_movie':user_favorite_movies,
          'user_added_cart':user_added_cart,


        } 
        return render(request,"category.html",context)
    
    if popularity=='Stars':
        if star is None:
            stars_with_count = StarsModel.objects.annotate(
            total_view_count=Sum('stars__view_count'),
            total_cart_count=Sum('stars__cart_count')
            )
        else:
            stars_with_count = star.annotate(
            total_view_count=Sum('stars__view_count'),
            total_cart_count=Sum('stars__cart_count')
            )
            
    

# Order the categories by total_view_count and total_cart_count
        sorted_stars = stars_with_count.order_by('-view_count','-total_view_count', '-total_cart_count')
        context={
          'genres':genres,
          'sort_stars':True,
          'data_dvd':get_dvd,
          'data_scene':get_scene,
          'data_photoset':get_photoset,
          'star':sorted_stars,
          'current':current,
          'haircolor':haircolor,
          'user_favourite_movie':user_favorite_movies,
          'user_added_cart':user_added_cart,
        } 
        return render(request,"category.html",context)


    context={
          'genres':genres,
          'data_dvd':get_dvd,
          'data_scene':get_scene,
          'data_photoset':get_photoset,
          'star':stardata,
          'current':current,
          'haircolor':haircolor,
          'user_favourite_movie':user_favorite_movies,
          'user_added_cart':user_added_cart,


     }
    return render(request,"category.html",context)

#simple categoy for genre
def category_by_genre(request,genrename):
     category=Category.objects.get(category_name=genrename)#first gets category
     genres=Category.objects.all()#get all genre to show as options
     datatoshow=MovieDetail.objects.all().filter(genre=category)[:20]#finally get movie based on category
     stardata=StarsModel.objects.all()
     current={}
     current['genre']=genrename
     context={
          'genres':genres,
          'data':datatoshow,
          'genre':genrename,
          'star':stardata,
          'current':current,

     }


     return render(request,"category.html",context)
