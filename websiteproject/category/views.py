from django.shortcuts import render
from .models import Category
from indexapp.models import MovieDetail,StarsModel,FavouritesModel,StudioModel
from detailapp.models import Cartitem
from django.db.models import  Sum
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse
from owner.models import Page
#Request to category page can be removed now as no category page is available now 
def category(request):
    pages=Page.objects.all().order_by('-id')
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
    age_ranges = [f"Age: {i}-{i+5}" for i in range(18, 40, 5)]
    attributes.append('Age')

    # Combine attribute names and values for the single <select> tag
    attribute_choices = []
    for attribute in attributes:
        if attribute == 'Age':
            attribute_choices.extend(age_ranges)
        else:
            values = StarsModel.objects.values(attribute_mapping[attribute]).distinct()
            values_list = [value[attribute_mapping[attribute]] for value in values]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])


    genres=Category.objects.all().order_by('-id')
    data=MovieDetail.objects.all()[:20]
    stardata=StarsModel.objects.all().order_by('-id')
    popular_genres= Category.objects.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]

    studio=StudioModel.objects.all().order_by('-id')
     
    context={
          'genres':genres,
          'data':data,
          'star':stardata,
          'popular_genre':popular_genres,
          'attributes':attribute_choices,
          'studio':studio,
          'pages':pages,
     }

    return render(request,"category.html",context)
    
#filtering mechanism which filters based on post data from index page
def category_filter(request,type=None):
    pages=Page.objects.all().order_by('-id')
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
            values_list = [value[attribute_mapping[attribute]] for value in values]
            attribute_choices.extend([f"{attribute}:{value}" for value in values_list])


    genres=Category.objects.all()
    all_studios=StudioModel.objects.all().order_by('-id')

    popular_category=None
    scene_category=None
    selected_options=None
    studio=None
    if 'popular_category' in request.POST:
         popular_category=request.POST.getlist('popular_category')
    if 'studio' in request.POST:
         studio=request.POST.getlist('studio')

    if 'scene_category' in request.POST:
        scene_category=request.POST.getlist('scene_category')
    if 'model' in request.POST:
        selected_options=request.POST.getlist('model')
    stars=None
    if selected_options is not None:
        selected_attributes = []
        selected_values = []
        for option in selected_options:
                attribute, value = option.split(':', 1)
                selected_attributes.append(attribute)
                selected_values.append(value)

        if selected_attributes and selected_values:
                selected_filters = {}
                for attribute, value in zip(selected_attributes, selected_values):


                    if "Age" in attribute:
                        # Extract the age range
                        min_age, max_age = map(int, value.split('-'))
                        min_year = datetime.now().year - max_age - 1
                        max_year = datetime.now().year - min_age
                        selected_filters['dob__year__gte'] = min_year
                        selected_filters['dob__year__lte'] = max_year
                    else:
                        field_name = attribute_mapping.get(attribute, attribute)
                        selected_filters[f'{field_name}'] = value

                stars = StarsModel.objects.filter(**selected_filters)



    movies=MovieDetail.objects.all()
    if stars is not None:
        movies=movies.filter(stars__in=stars)
    
    if popular_category is not None:
        movies=movies.filter(genre__in=popular_category)
    if scene_category is not None:
        movies=movies.filter(genre__in=scene_category)
    if studio is not None:
        movies=movies.filter(studio__in=studio)
    
  
    current={}
    current['popular_category']=popular_category
    current['all_category']=scene_category
    current['choice']=selected_options
    current['studio']=studio


    ###To deterrmine which filters are applied
    if type is not None:
        data_to_show="data_"+type.lower()
        actual_data=movies.filter(type=type,quality="HD").order_by('-id')
        paginator_data=Paginator(actual_data,20)
        page_data=request.GET.get('page_'+type.lower())
        paged_data=paginator_data.get_page(page_data)

    else:   
    # now getting data based on type
        get_dvd=movies.filter(type="DVD",quality="HD").order_by('-id')
        paginator_dvd=Paginator(get_dvd,20)
        page_dvd=request.GET.get('page_dvd')
        paged_dvd=paginator_dvd.get_page(page_dvd)

        get_scene=movies.filter(type="Scene",quality="HD").order_by('-id')
        paginator_scene=Paginator(get_scene,20)
        page_scene=request.GET.get('page_scene')
        paged_scene=paginator_scene.get_page(page_scene)

        get_photoset=movies.filter(type="PhotoSets",quality="HD").order_by('-id')
        paginator_photosets=Paginator(get_photoset,20)
        page_photo=request.GET.get('page_photosets')
        paged_photo=paginator_photosets.get_page(page_photo)

    stardata=StarsModel.objects.all()
    haircolor=StarsModel.objects.values('haircolor').distinct()
    
    user_favorite_movies=None
    if  not isinstance(request.user, AnonymousUser):# same as request.user.is_authenticated
        user_favorite_movies = FavouritesModel.objects.filter(user=request.user).values_list('favourite_movies__id', flat=True)
    user_added_cart=None
    if not isinstance(request.user,AnonymousUser):
        user_added_cart=Cartitem.objects.filter(user=request.user).values_list('product__id',flat=True)

    popular_genres=Category.objects.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        actual_data=None
        response_data=None
        page_scene = request.GET.get('page_scene')
        page_dvd=request.GET.get('page_dvd')
        page_photo=request.GET.get('page_photosets')
        page_sort=request.GET.get('sort')
        page_view=request.GET.get('view')
        page_display=request.GET.get('display')   

        if page_sort is not None:
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
            paginator_scene=Paginator(actual_data.filter(type="Scene"),page_number)
            paginator_dvd=Paginator(actual_data.filter(type="DVD"),page_number)
            paginator_photosets=Paginator(actual_data.filter(type="PhotoSets"),page_number)

            page_dvd=request.GET.get('page_dvd')
            paged_dvd=paginator_dvd.get_page(page_dvd)
            page_scene=request.GET.get('page_scene')
            paged_scene=paginator_scene.get_page(page_scene)
            page_photosets=request.GET.get('page_photosets')
            paged_photo=paginator_photosets.get_page(page_photosets)
            

            if page_dvd is None and type is None and page_photo is None and page_scene is None:
                context={
                     'data_dvd':paged_dvd,
                        'data_scene':paged_scene,
                        'data_photosets':paged_photo,
                        'user_favourite_movie':user_favorite_movies,
                        'user_added_cart':user_added_cart,
                }
                html=render_to_string('partial/partial-category.html',context)
                response_data={
                    'content':html
                }
                return JsonResponse(response_data)


        if type is not None:
            if actual_data is  None:
                actual_data=movies.filter(type=type,quality="HD").order_by('-id')
            else:
                actual_data=actual_data.filter(type=type)
            paginator_data=Paginator(actual_data,page_number)

            page_data=request.GET.get('page_'+type.lower())
            paged_data=paginator_data.get_page(page_data)
            if type.lower()=="dvd":
                dvd_html = render_to_string('partial/dvd_partial.html', {'dvd': paged_data}, request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_data,'type':"dvd",}, request=request)
                response_data = {
                'content': dvd_html,
                'pagination': pagination_html,
                    }
            elif type.lower()=="scene":
                scenes_html = render_to_string('partial/scenes_partial.html', {'scenes': paged_data}, request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_data,'type':"scene",}, request=request)
                response_data = {
                'content': scenes_html,
                'pagination': pagination_html,
                }
            else:
                photo_html = render_to_string('partial/photo_partial.html', {'photoset': paged_data}, request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_data,'type':"photosets",}, request=request)
                response_data = {
            'content': photo_html,
            'pagination': pagination_html,
                }
            return JsonResponse(response_data)


        if page_scene is not None:
            paged_scene = paginator_scene.get_page(page_scene)
            scenes_html = render_to_string('partial/scenes_partial.html', {'scenes': paged_scene}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_scene,'type':"scene",}, request=request)
            response_data = {
        'content': scenes_html,
        'pagination': pagination_html,
            }

        if page_dvd is not None:
            paged_dvd= paginator_dvd.get_page(page_dvd)
            dvd_html = render_to_string('partial/dvd_partial.html', {'dvd': paged_dvd}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_dvd,'type':"dvd",}, request=request)
            response_data = {
        'content': dvd_html,
        'pagination': pagination_html,
            }

        if page_photo is not None:
            paged_photo= paginator_photosets.get_page(page_photo)
            photo_html = render_to_string('partial/photo_partial.html', {'photoset': paged_photo}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_photo,'type':"photosets",}, request=request)
            response_data = {
        'content': photo_html,
        'pagination': pagination_html,
            }

        return JsonResponse(response_data)


    if type is not None:
        context={
          'genres':genres,
           data_to_show:paged_data,#gives paged_dvd or anyother type depending on req
           'type':type,
          'star':stardata,
          'haircolor':haircolor,
          'user_favourite_movie':user_favorite_movies,
          'user_added_cart':user_added_cart,
          'attributes':attribute_choices,
          'popular_genre':popular_genres,
          'current':current,
          'studio':all_studios,
          'pages':pages,
        }

    else:
# Order the categories by total_view_count and total_cart_count
        context={
            'genres':genres,
            'data_dvd':paged_dvd,
            'data_scene':paged_scene,
            'data_photosets':paged_photo,
            'star':stardata,
            'haircolor':haircolor,
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'attributes':attribute_choices,
            'popular_genre':popular_genres,
            'current':current,
            'studio':all_studios,
            'pages':pages,

            } 
    return render(request,"category.html",context)
    
   
#simple categoy for genre
def category_by_genre(request,genrename):
     pages=Page.objects.all().order_by('-id')
     category=Category.objects.get(category_name=genrename)#first gets category
     genres=Category.objects.all()#get all genre to show as options
     datatoshow=MovieDetail.objects.all().filter(genre=category)#finally get movie based on category
     get_dvd=datatoshow.filter(type="DVD",quality="HD").order_by('-id')
     
     paginator_dvd=Paginator(get_dvd,20)
     page_dvd=request.GET.get('page_dvd')
     paged_dvd=paginator_dvd.get_page(page_dvd)

     get_scene=datatoshow.filter(type="Scene",quality="HD").order_by('-id')
     paginator_scene=Paginator(get_scene,20)
     page_scene=request.GET.get('page_scene')
     paged_scene=paginator_scene.get_page(page_scene)

     get_photoset=datatoshow.filter(type="PhotoSets",quality="HD").order_by('-id')
     paginator_photosets=Paginator(get_photoset,20)
     page_photo=request.GET.get('page_photosets')
     paged_photo=paginator_photosets.get_page(page_photo)
     stardata=StarsModel.objects.all()

     context={
          'genres':genres,
          'data_dvd':paged_dvd,
          'data_scene':paged_scene,
          'data_photosets':paged_photo,
          'genre':genrename,
          'star':stardata,
          'pages':pages,

     }

     return render(request,"category.html",context)
