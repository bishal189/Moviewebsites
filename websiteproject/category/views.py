from django.shortcuts import render
from .models import Category
from indexapp.models import MovieDetail,StarsModel,FavouritesModel
from detailapp.models import Cartitem
from django.db.models import  Sum
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import Lower

#Request to category page can be removed now as no category page is available now 
def category(request):
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
    popular_genres=popular_categories = Category.objects.annotate(
    total_views=Count('moviedetail__view_count'),
    total_carts=Count('moviedetail__cart_count')
    ).order_by('-total_views', '-total_carts')[:10]
     


    context={
          'genres':genres,
          'data':data,
          'star':stardata,
          'popular_genre':popular_genres,
          'attributes':attribute_choices,
     }

    return render(request,"category.html",context)
    
#filtering mechanism which filters based on post data from index page
def category_filter(request,type=None):
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

    ###Get all data from post
    popular_category=None
    scene_category=None
    selected_options=None
    view=None
    sort=None
    if 'popular_category' in request.POST:
         popular_category=request.POST.getlist('popular_category')

    if 'scene_category' in request.POST:
        scene_category=request.POST.getlist('scene_category')
    if 'model' in request.POST:
        selected_options=request.POST.getlist('model')
    if 'view' in request.POST:
        view=request.POST['view']
    if 'sort' in request.POST:
        sort=request.POST['sort']
    ####
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

    if sort is not None and sort!="":
        
        if sort=="newest":

            movies=MovieDetail.objects.all().order_by('-id')
        if sort=="alphabetical":
            movies = MovieDetail.objects.all().order_by(Lower('movie_name'))
        if sort=="most-trending":
            movies=MovieDetail.objects.all().order_by('-cart_count')
        if sort=="most-popular":
            movies=MovieDetail.objects.all().order_by('-view_count','-cart_count','-id')
    else:
        movies=MovieDetail.objects.all()
    if stars is not None:
        movies=movies.filter(stars__in=stars)
    
    
    
    if popular_category is not None:
        movies=movies.filter(genre__in=popular_category)
    if scene_category is not None:
        movies=movies.filter(genre__in=scene_category)
    
    if view is not None and view != "":
        movies=movies.filter(quality=view)
    
   
    current={}
    current['view']=view
    current['sort']=sort
    current['popular_category']=popular_category
    current['all_category']=scene_category
    current['choice']=selected_options


    ###To deterrmine which filters are applied
    if type is not None:
        data_to_show="data_"+type.lower()
        
        actual_data=movies.filter(type=type)

    else:   
    # now getting data based on type
        get_dvd=movies.filter(type="DVD")
        get_scene=movies.filter(type="Scene")
        get_photoset=movies.filter(type="PhotoSets")

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


    if type is not None:
        context={
          'genres':genres,
           data_to_show:actual_data,
           'type':type,
          'star':stardata,
          'haircolor':haircolor,
          'user_favourite_movie':user_favorite_movies,
          'user_added_cart':user_added_cart,
          'attributes':attribute_choices,
          'popular_genre':popular_genres,
          'current':current,
        }

    else:
# Order the categories by total_view_count and total_cart_count
        context={
            'genres':genres,
            'data_dvd':get_dvd,
            'data_scene':get_scene,
            'data_photosets':get_photoset,
            'star':stardata,
            'haircolor':haircolor,
            'user_favourite_movie':user_favorite_movies,
            'user_added_cart':user_added_cart,
            'attributes':attribute_choices,
            'popular_genre':popular_genres,
            'current':current,

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
