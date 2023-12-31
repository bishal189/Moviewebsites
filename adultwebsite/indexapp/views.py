from django.shortcuts import render,get_object_or_404
from .models import MovieDetail,StarsModel,StudioModel
from indexapp.models import Category,FavouritesModel
from django.core.paginator import Paginator
# Create your views here.
from django.http import JsonResponse
from albums.models import Albums
from datetime import datetime
from django.contrib.auth.models import AnonymousUser
from detailapp.models import Cartitem
from django.template.loader import render_to_string
from owner.models import Page
from django.db.models import Count
from django.db.models.functions import Lower


#Home page
def home(request): 
    lang=request.LANGUAGE_CODE

    #just for showing filtering data
    attribute_mapping = {
        'Hair Color': 'haircolor',
        'Ethnicity': 'ethnicity',
        'Nationality': 'nationality',
        'Eye Color': 'eyecolor',
        'Body Type': 'bodytype',
        'Body Piercing': 'piercing',
        'Boob Size': 'breastsize',
        'Boob Type': 'breasttype',
        'Body Markings':'bodymarking',
        'Current Status':'currentstatus',
        'Gender':'gender',

    }

    attributes = list(attribute_mapping.keys())

    age_ranges = [f"Age: {i}-{i+5}" for i in range(18, 50, 5)]
    attributes.append('Age')

    # Combine attribute names and values for the single <select> tag
    attribute_choices = []
    for attribute in attributes:
        if attribute == 'Age':
            attribute_choices.extend(age_ranges)
        else:
            values = StarsModel.objects.values(attribute_mapping[attribute]).distinct()
            values_list = [value[attribute_mapping[attribute]] for value in values if value[attribute_mapping[attribute]] is not None]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])
    
    genres=Category.objects.filter(lang=lang).order_by('-id')
   
    popular_genres= genres.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]
    studio=StudioModel.objects.filter(lang=lang).order_by('-id')

# end attribute for showing data in model star for filtering 

    movies=MovieDetail.objects.filter(lang=lang)
    all_dvd=movies.filter(type="DVD").order_by('-id')
    all_scene=movies.filter(type="Scene").order_by('-id')
    all_photosets=movies.filter(type="PhotoSets").order_by('-id')

    paginator_dvd=Paginator(all_dvd,10)
    page_dvd=request.GET.get('page_dvd')
    paged_dvd=paginator_dvd.get_page(page_dvd)

    paginator_scene=Paginator(all_scene,10)
    page_scene=request.GET.get('page_scene')
    paged_scene=paginator_scene.get_page(page_scene)

    paginator_photo=Paginator(all_photosets,10)
    page_photo=request.GET.get('page_photo')
    paged_photo=paginator_photo.get_page(page_photo)

    count_dvd=all_dvd.count()
    allalbums=Albums.objects.filter(lang=lang).order_by('-id')
    paginator_album=Paginator(allalbums,10)
    page_album=request.GET.get('page_album')
    paged_album=paginator_album.get_page(page_album)

    stardata=StarsModel.objects.all().order_by('-view_count')
    paginator_star=Paginator(stardata,12)
    page_star=request.GET.get('page_star')
    paged_star=paginator_star.get_page(page_star)

    haircolor=StarsModel.objects.values('haircolor').distinct()

    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    # count1=paged_products.count()
    #if the request is fetch request with page then page shouldnot load
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':

        response_data=None
        page_scene = request.GET.get('page_scene')
        page_dvd=request.GET.get('page_dvd')
        page_photo=request.GET.get('page_photo')
        page_star=request.GET.get('page_star')
        page_album=request.GET.get('page_album')

        if page_scene is not None:
            paged_scene = paginator_scene.get_page(page_scene)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'scenes':paged_scene
            }
            
            scenes_html = render_to_string('partial/scenes_partial.html',context, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_scene,'type':"scene",}, request=request)
            response_data = {
        'content': scenes_html,
        'pagination': pagination_html,
            }

        if page_dvd is not None:
            paged_dvd= paginator_dvd.get_page(page_dvd)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'dvd':paged_dvd
            }
            dvd_html = render_to_string('partial/dvd_partial.html',context, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_dvd,'type':"dvd",}, request=request)
            response_data = {
        'content': dvd_html,
        'pagination': pagination_html,
            }

        if page_photo is not None:
            paged_photo= paginator_photo.get_page(page_photo)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'photoset':paged_photo
            }
            photo_html = render_to_string('partial/photo_partial.html',context, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_photo,'type':"photo",}, request=request)
            response_data = {
        'content': photo_html,
        'pagination': pagination_html,
            }
        if page_album is not None:
            paged_album=paginator_album.get_page(page_album)

            album_html=render_to_string('partial/album_partial.html',{'albums':paged_album},request=request)
            pagination_html=render_to_string('partial/pagination_partial.html',{'data':paged_album,'type':'album'})
            response_data={
                'content':album_html,
                'pagination':pagination_html
            }
        if page_star is not None:
            paged_star= paginator_star.get_page(page_star)
            star_html = render_to_string('partial/star_partial.html', {'star': paged_star}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_star,'type':"star",}, request=request)
            response_data = {
        'content': star_html,
        'pagination': pagination_html,
            }
        return JsonResponse(response_data)
    
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')

    context={
        'genres':genres,
        'dvd':paged_dvd,
        'scenes':paged_scene,
        'photoset':paged_photo,
        'count':count_dvd,
        'allalbums':paged_album,
        'star':paged_star,     
        'haircolor':haircolor,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        'pages':pages,
        'popular_genre':popular_genres,
        'attributes':attribute_choices,
        'studio':studio   
    }


    return render(request,'index.html',context)


#Studo Detail page which shows all list of items done by that studio 
def studio_detail(request,id):
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
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
        'pages':pages,

    }
    return render(request,'studio-detail.html',context)

#Searching functionality
def search(request):
    lang=request.LANGUAGE_CODE
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    tosearch=request.POST['searchtext']
    movies=MovieDetail.objects.filter(lang=lang)
    get_dvd=movies.filter(movie_name__icontains=tosearch,type="DVD").order_by('-id')
    get_scene=movies.filter(movie_name__icontains=tosearch,type="Scene").order_by('-id')
    get_photoset=movies.filter(movie_name__icontains=tosearch,type="PhotoSets").order_by('-id')
    get_album=Albums.objects.filter(lang=lang,album_name__icontains=tosearch).order_by('-id')
   
    paginator_dvd = Paginator(get_dvd, per_page=10)
    paginator_scene=Paginator(get_scene,per_page=10)  # Set the number of items per page (e.g., 10 items per page)
   
    page_number_dvd = request.GET.get('page_dvd') 
    page_number_scene=request.GET.get('page_scene') # Get the current page number from the request
   
    paged_products_dvd = paginator_dvd.get_page(page_number_dvd)  # Get the Page object for the current page
    paged_products_scene = paginator_scene.get_page(page_number_scene)  # Get the Page object for the current page
    
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
        'pages':pages,
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

#Getting list of scene type Movies
def scenes(request):
    lang=request.LANGUAGE_CODE
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    #just for showing filtering data
    attribute_mapping = {
        'Hair Color': 'haircolor',
        'Ethnicity': 'ethnicity',
        'Nationality': 'nationality',
        'Eye Color': 'eyecolor',
        'Body Type': 'bodytype',
        'Body Piercing': 'piercing',
        'Boob Size': 'breastsize',
        'Boob Type': 'breasttype',
        'Body Markings':'bodymarking',
        'Current Status':'currentstatus',
        'Gender':'gender',

    }

    attributes = list(attribute_mapping.keys())

    age_ranges = [f"Age: {i}-{i+5}" for i in range(18, 50, 5)]
    attributes.append('Age')

    # Combine attribute names and values for the single <select> tag
    attribute_choices = []
    for attribute in attributes:
        if attribute == 'Age':
            attribute_choices.extend(age_ranges)
        else:
            values = StarsModel.objects.values(attribute_mapping[attribute]).distinct()
            values_list = [value[attribute_mapping[attribute]] for value in values if value[attribute_mapping[attribute]] is not None]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])
    
    genres=Category.objects.filter(lang=lang).order_by('-id')
    popular_genres= genres.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]
    
    studio=StudioModel.objects.filter(lang=lang).order_by('-id')

# end attribute for showing data in model star for filtering 

    alldata = MovieDetail.objects.filter(lang=lang,type='Scene').order_by('-id')
    paginator_scene = Paginator(alldata, 20)
    page_scene = request.GET.get('page_scene')
    paged_scene = paginator_scene.get_page(page_scene)

    user_favorite_movies = None
    if not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)

    user_added_cart = None
    if not isinstance(request.user, AnonymousUser):
        user_added_cart = Cartitem.objects.filter(user=request.user).values_list('product__id', flat=True)    
    
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        page_sort=request.GET.get('sort')
        page_view=request.GET.get('view')
        page_display=request.GET.get('display')   
        page_scene=request.GET.get('page_scene')
        if page_sort is not None:
            if page_view=='all':
                actual_data_quality=alldata
            else:
                actual_data_quality=alldata.filter(quality=page_view)

            if page_sort=="newest":
                actual_data=actual_data_quality.order_by('-id')
            if page_sort=="alphabetical":
                actual_data = actual_data_quality.order_by(Lower('movie_name'))
            if page_sort=="most-trending":
                 actual_data=actual_data_quality.order_by('-cart_count')
            if page_sort=="most-popular":
                actual_data=actual_data_quality.order_by('-view_count','-cart_count','-id')
            
            page_number=page_display
            paginator_scene=Paginator(actual_data.filter(type="Scene"),page_number)
            

            if page_scene is None:
                paged_scene = paginator_scene.get_page(page_scene)
                context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'scenes':paged_scene
            }
                html=render_to_string('partial/scenes_partial.html',context,request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_scene,'type':"scene",}, request=request)

                response_data={
                    'content':html,
                    'pagination':pagination_html,
                }

        if page_scene is not None:
            paged_scene = paginator_scene.get_page(page_scene)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'scenes':paged_scene
            }
            scenes_html = render_to_string('partial/scenes_partial.html',context, request=request)

        # Render the pagination HTML
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_scene,'type':"scene",}, request=request)

            response_data = {
            'content': scenes_html,
            'pagination': pagination_html,
            }
        
        return JsonResponse(response_data)

    context={
        'scenes':paged_scene,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        'genres':genres,
        'popular_genre':popular_genres,
        'attributes':attribute_choices,
        'studio':studio,
        'pages':pages,
    }
    return render(request, 'scenes.html',context)

def dvd(request):
    lang=request.LANGUAGE_CODE
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    #just for showing filtering data
    attribute_mapping = {
        'Hair Color': 'haircolor',
        'Ethnicity': 'ethnicity',
        'Nationality': 'nationality',
        'Eye Color': 'eyecolor',
        'Body Type': 'bodytype',
        'Body Piercing': 'piercing',
        'Boob Size': 'breastsize',
        'Boob Type': 'breasttype',
        'Body Markings':'bodymarking',
        'Current Status':'currentstatus',
        'Gender':'gender',

    }

    attributes = list(attribute_mapping.keys())

    age_ranges = [f"Age: {i}-{i+5}" for i in range(18, 50, 5)]
    attributes.append('Age')

    # Combine attribute names and values for the single <select> tag
    attribute_choices = []
    for attribute in attributes:
        if attribute == 'Age':
            attribute_choices.extend(age_ranges)
        else:
            values = StarsModel.objects.values(attribute_mapping[attribute]).distinct()
            values_list = [value[attribute_mapping[attribute]] for value in values if value[attribute_mapping[attribute]] is not None]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])


# end attribute for showing data in model star for filtering 
    studio=StudioModel.objects.filter(lang=lang)
    alldata=MovieDetail.objects.filter(lang=lang,type='DVD').order_by('-id')
    paginator_dvd=Paginator(alldata,20)
    page_dvd=request.GET.get('page_dvd')
    paged_dvd=paginator_dvd.get_page(page_dvd)
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
    # count1=paged_products.count()


    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        response_data=None

        page_sort=request.GET.get('sort')
        page_view=request.GET.get('view')
        page_display=request.GET.get('display')   
        page_dvd=request.GET.get('page_dvd')
        if page_sort is not None:
            if page_view=="all":
                actual_data_quality=alldata
            else:
                actual_data_quality=alldata.filter(quality=page_view)
            if page_sort=="newest":
                actual_data=actual_data_quality.order_by('-id')
            if page_sort=="alphabetical":
                actual_data = actual_data_quality.order_by(Lower('movie_name'))
            if page_sort=="most-trending":
                 actual_data=actual_data_quality.order_by('-cart_count')
            if page_sort=="most-popular":
                actual_data=actual_data_quality.order_by('-view_count','-cart_count','-id')
            
            page_number=page_display
            paginator_dvd=Paginator(actual_data.filter(type="DVD"),page_number)
            

            if page_dvd is None:
                paged_dvd=paginator_dvd.get_page(page_dvd)
                context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'dvd':paged_dvd
            }
                html=render_to_string('partial/dvd_partial.html',context,request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_dvd,'type':"dvd",}, request=request)

                response_data={
                    'content':html,
                    'pagination':pagination_html
                }


        if page_dvd is not None:
            paged_dvd= paginator_dvd.get_page(page_dvd)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'dvd':paged_dvd
            }
            dvd_html = render_to_string('partial/dvd_partial.html', context, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_dvd,'type':"dvd",}, request=request)
            response_data = {
        'content': dvd_html,
        'pagination': pagination_html,
            }
        return JsonResponse(response_data)
    
    genres=Category.objects.filter(lang=lang).order_by('-id')

    popular_genres= genres.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]

    context={
        'dvd':paged_dvd,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        'genres':genres,
        'popular_genre':popular_genres,
        'attributes':attribute_choices,
        'studio':studio,
        'pages':pages,

    }


    return render(request,'dvd.html',context)

def stars(request):
    
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    allstars=StarsModel.objects.all().order_by('-id')
    paginator_star=Paginator(allstars,12)
    page_star=request.GET.get('page_star')
    paged_star=paginator_star.get_page(page_star)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        response_data=None
        page_stars=request.GET.get('page_star')
        if page_stars is not None:
            paged_star= paginator_star.get_page(page_star)
            star_html = render_to_string('partial/star_partial.html', {'star': paged_star}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_star,'type':"star",}, request=request)
            response_data = {
        'content': star_html,
        'pagination': pagination_html,
            }
        return JsonResponse(response_data)

    context={
        'star':paged_star,
        'pages':pages,
    }
    return render(request,'stars.html',context)
    

def star_detail(request,id):
    lang=request.LANGUAGE_CODE
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    star=StarsModel.objects.get(id=id)
    star.view_count=star.view_count+1
    star.save()
    if star.dob is not None:
        dob=star.dob
        current_date = datetime.now()
        age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    else:
        age=None
    movies=MovieDetail.objects.filter(lang=lang,stars=star)
    data_dvd=movies.filter(type="DVD").order_by('-id')
    data_scene=movies.filter(type="Scene").order_by('-id')

    data_photoset=movies.filter(type="PhotoSets").order_by('-id')
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)

    context={
        'star':star,
        'data_dvd':data_dvd,
        'data_scene':data_scene,
        'data_photoset':data_photoset,
        'age':age,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        'pages':pages,

    }
    return render(request,'stardetail.html',context)


def photosets(request):
    lang=request.LANGUAGE_CODE

    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    #just for showing filtering data
    attribute_mapping = {
        'Hair Color': 'haircolor',
        'Ethnicity': 'ethnicity',
        'Nationality': 'nationality',
        'Eye Color': 'eyecolor',
        'Body Type': 'bodytype',
        'Body Piercing': 'piercing',
        'Boob Size': 'breastsize',
        'Boob Type': 'breasttype',
        'Body Markings':'bodymarking',
        'Current Status':'currentstatus',
        'Gender':'gender',

    }

    attributes = list(attribute_mapping.keys())

    age_ranges = [f"Age: {i}-{i+5}" for i in range(18, 50, 5)]
    attributes.append('Age')

    # Combine attribute names and values for the single <select> tag
    attribute_choices = []
    for attribute in attributes:
        if attribute == 'Age':
            attribute_choices.extend(age_ranges)
        else:
            values = StarsModel.objects.values(attribute_mapping[attribute]).distinct()
            values_list = [value[attribute_mapping[attribute]] for value in values if value[attribute_mapping[attribute]] is not None]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])

# end attribute for showing data in model star for filtering 
    studio=StudioModel.objects.filter(lang=lang).order_by('-id')
    genres=Category.objects.filter(lang=lang).order_by('-id')

    popular_genres= genres.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]

    movies=MovieDetail.objects.filter(lang=lang,type="PhotoSets")
    paginator_photo=Paginator(movies,20)
    page_photo=request.GET.get('page_photo')
    paged_photo=paginator_photo.get_page(page_photo)


    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)
  
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        response_data=None
        page_sort=request.GET.get('sort')
        page_view=request.GET.get('view')
        page_display=request.GET.get('display')   
        page_photo=request.GET.get('page_photo')
        if page_sort is not None:
            if page_view=="all":
                actual_data_quality=movies
            else:
                actual_data_quality=movies.filter(quality=page_view)
            if page_sort=="newest":

                actual_data=actual_data_quality.order_by('-id')
            if page_sort=="alphabetical":
                actual_data = actual_data_quality.order_by(Lower('movie_name'))
            if page_sort=="most-trending":
                 actual_data=actual_data_quality.order_by('-cart_count')
            if page_sort=="most-popular":
                actual_data=actual_data_quality.order_by('-view_count','-cart_count','-id')
            
            page_number=page_display
            paginator_photo=Paginator(actual_data.filter(type="PhotoSets"),page_number)
            

            if page_photo is None:
                paged_photo=paginator_photo.get_page(page_photo)

                context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'photoset':paged_photo
            }
                html=render_to_string('partial/photo_partial.html',context,request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_photo,'type':"photo",}, request=request)

                response_data={
                    'content':html,
                    'pagination':pagination_html
                }

        if page_photo is not None:
            
            paged_photo= paginator_photo.get_page(page_photo)
            context={
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'photoset':paged_photo
            }
            photo_html = render_to_string('partial/photo_partial.html', context, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_photo,'type':"photo",}, request=request)
            response_data = {
        'content': photo_html,
        'pagination': pagination_html,

            }
        return JsonResponse(response_data)


    context={
        'photoset':paged_photo,
        'user_favourite_movie':user_favorite_movies,
        'user_added_cart':user_added_cart,
        'genres':genres,
        'popular_genre':popular_genres,
        'attributes':attribute_choices,
        'studio':studio,
        'pages':pages,
        
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



def pageshow(request,slug):
    pages=Page.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
    page=Page.objects.get(slug=slug)
    context={
        'page':page,
        'pages':pages
    }
    return render(request,'page-template.html',context)


