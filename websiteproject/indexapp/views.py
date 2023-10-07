from django.shortcuts import render,get_object_or_404
from .models import MovieDetail,StarsModel,StudioModel
from indexapp.models import Category,FavouritesModel
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
from django.http import JsonResponse
from albums.models import Albums
from datetime import datetime
from django.contrib.auth.models import AnonymousUser
from detailapp.models import Cartitem

def home(request):
   
    all_dvd=MovieDetail.objects.filter(type="DVD").order_by('-id')
    all_scene=MovieDetail.objects.filter(type="Scene").order_by('-id')
    all_photosets=MovieDetail.objects.filter(type="PhotoSets").order_by('-id')

    paginator_dvd=Paginator(all_dvd,20)
    page_dvd=request.GET.get('page_dvd')
    paged_dvd=paginator_dvd.get_page(page_dvd)

    paginator_scene=Paginator(all_scene,6)
    page_scene=request.GET.get('page_scene')
    paged_scene=paginator_scene.get_page(page_scene)

    paginator_photo=Paginator(all_photosets,5)
    page_photo=request.GET.get('page_photo')
    paged_photo=paginator_photo.get_page(page_photo)

    # paginator_dvd=Paginator(all_dvd,5)
    # page_dvd=request.GET.get('page')
    # paged_dvd=paginator_dvd.get_page(page_dvd)
    



    count_dvd=all_dvd.count()
    allalbums=Albums.objects.all().order_by('-id')
    stardata=StarsModel.objects.all().order_by('-view_count')
    paginator_star=Paginator(stardata,5)
    page_star=request.GET.get('page_star')
    paged_star=paginator_star.get_page(page_star)


    genres=Category.objects.all().order_by('-id')
    haircolor=StarsModel.objects.values('haircolor').distinct()

    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    # count1=paged_products.count()
    context={
        'genres':genres,
        'all_dvd':paged_dvd,
        'all_scene':paged_scene,
        'all_photoset':paged_photo,
        'count':count_dvd,
        'allalbums':allalbums,
        'star':paged_star,
        
        'haircolor':haircolor,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        
    }
    return render(request,'index.html',context)
    
def studio_detail(request,id):
    studio=StudioModel.objects.get(id=id)
    movies=MovieDetail.objects.filter(studio=studio)
    dvd=movies.filter(type='DVD').order_by('-id')
    photo_sets=movies.filter(type='PhotoSets').order_by('-id')
    scene=movies.filter(type='Scene').order_by('-id')
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)

    context={
        'product':studio,
        'movies':movies,
        'dvd':dvd,
        'photoset':photo_sets,
        'scene':scene,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,

    }
    return render(request,'studio-detail.html',context)
def search(request):
    tosearch=request.POST['searchtext']
    get_dvd=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="DVD").order_by('-id')
    get_scene=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="Scene").order_by('-id')
    get_photoset=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="PhotoSets").order_by('-id')
    get_album=Albums.objects.filter(album_name__icontains=tosearch).order_by('-id')
    # paginator_dvd = Paginator(get_dvd, per_page=10)
    # paginator_scene=Paginator(get_scene,per_page=10)  # Set the number of items per page (e.g., 10 items per page)
    # page_number_dvd = request.GET.get('page_dvd') 
    # page_number_scene=request.GET.get('page_scene') # Get the current page number from the request
    # paged_products_dvd = paginator_dvd.get_page(page_number_dvd)  # Get the Page object for the current page
    # paged_products_scene = paginator_scene.get_page(page_number_scene)  # Get the Page object for the current page
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    # count1=paged_products.count()

    
    context={
        'all_products_dvd':get_dvd,
        'photo_set':get_photoset,
        'album':get_album,
        'tosearch':tosearch,
        'all_products_scene':get_scene,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,

        
        
    }
    return render(request,'search.html',context)

def search_pagination(request,tosearch):
    get_dvd=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="DVD")
    get_scene=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="Scene")
    paginator1=Paginator(get_scene,per_page=1) 
    paginator = Paginator(get_dvd, per_page=1)
    page_number1=request.GET.get('page')
    paged_products1 = paginator1.get_page(page_number1)   # Set the number of items per page (e.g., 10 items per page)
    page_number = request.GET.get('page')  # Get the current page number from the request
    paged_products = paginator.get_page(page_number)  # Get the Page object for the current page
    context={
        'data1':get_scene,
        'all_products':paged_products,
        'all_products1':paged_products1,
        'tosearch':tosearch,
        
        
    }
    return render(request,'search.html',context)


def pagination(request):
    all_product=MovieDetail.objects.all().order_by('id')
    paginator=Paginator(all_product,1)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)

    count=all_product.count()
    context={
        'all_products':paged_products,
        'count':count,
        
    }
    return render(request,'index.html',context)



def scenes(request):
    alldata=MovieDetail.objects.filter(type='Scene')
    paginator_scene=Paginator(alldata,4)
    page_scene=request.GET.get('page')
    paged_scene=paginator_scene.get_page(page_scene)
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    
    return render(request,'scenes.html',{'scenes':paged_scene,'user_favourite_movie':user_favorite_movies,'user_added_cart':user_added_cart})


def dvd(request):
    alldata=MovieDetail.objects.filter(type='DVD')
    paginator_scene=Paginator(alldata,4)
    page_scene=request.GET.get('paged_dvd')
    paged_scene=paginator_scene.get_page(page_scene)
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    # count1=paged_products.count()
    return render(request,'dvd.html',{'alldata':alldata,'paged_dvd':paged_scene ,'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart
})

def stars(request):
    allstars=StarsModel.objects.all().order_by('-id')
    paginator_scene=Paginator(allstars,4)
    page_scene=request.GET.get('stars')
    paged_scene=paginator_scene.get_page(page_scene)
    context={
        'stars':paged_scene,
    }
    return render(request,'stars.html',context)
    
def star_detail(request,id):
    star=StarsModel.objects.get(id=id)
    star.view_count=star.view_count+1

    star.save()
    if star.dob is not None:
        dob=star.dob
        current_date = datetime.now()
        age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    else:
        age=None
    movies=MovieDetail.objects.filter(stars=star)
    context={
        'star':star,
        'movies':movies,
        'age':age,
    }
    return render(request,'stardetail.html',context)


def photosets(request):
    movies=MovieDetail.objects.filter(type="PhotoSets")
   
    paginator_scene=Paginator(movies,4)
    page_scene=request.GET.get('photosets')
    paged_scene=paginator_scene.get_page(page_scene)
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)

    context={
        'movies':paged_scene,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        
    }

    return render(request,'photosets.html',context)


def add_favourites(request,id):
    user=request.user
    favourite,created=FavouritesModel.objects.get_or_create(user=user)
    movie=MovieDetail.objects.get(id=id)
    favourite.favourite_movies.add(movie)
    favourite.save()
    return JsonResponse({"status":"done"})

def remove_favourites(request,id):
    user=request.user
    favourite=FavouritesModel.objects.get(user=user)
    movie=MovieDetail.objects.get(id=id)
    favourite.favourite_movies.remove(movie)
    favourite.save()
    return JsonResponse({"status":"done"})



def about(request):
    return render(request,'about.html')
def privacy(request):
    return render(request,'privacy.html')


