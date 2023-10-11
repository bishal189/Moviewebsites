from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums,AlbumMovie,Separator
from django.http import JsonResponse
from django.core.paginator import Paginator
from detailapp.models import Cartitem,Order_Product_album,Order_Product
from django.template.loader import render_to_string

#for getting the list of albums in album page
def album(request):
    albums=Albums.objects.all()
    paginator_album=Paginator(albums,12)
    page_album=request.GET.get('page_albums')
    paged_album=paginator_album.get_page(page_album)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
        response_data=None
        page_album=request.GET.get('page_albums')
        if page_album is not None:
            paged_album= paginator_album.get_page(page_album)
            album_html = render_to_string('partial/album_partial.html', {'albums': paged_album}, request=request)
            pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_album,'type':"albums",}, request=request)
            response_data = {
        'content': album_html,
        'pagination': pagination_html,
            }
        return JsonResponse(response_data)

    context={
        'albums':paged_album
    }
    return render(request,'album.html',context)


#for getting the particular album besed on id
def album_detail(request,id):
    album=Albums.objects.get(id=id) 
    movies=MovieDetail.objects.filter(genre__in=album.genre.all(),type=album.type).order_by('-id').distinct()
    counter=0

    #since previous movies which are alraedy bough should not be shown
    previous_movies_in_albums_bought=[]
    if request.user.is_authenticated:
        previous_album=Order_Product_album.objects.filter(user=request.user)
        for item in previous_album:
            previous_movies=item.product.movies.all()
            previous_movies_in_albums_bought.append(previous_movies)

    #alraedy in album should be shown added in button
    already_in_album=None
    if request.user.is_authenticated:
        globaldata,created=Separator.objects.get_or_create(user=request.user)
        albummovie,created=AlbumMovie.objects.get_or_create(user=request.user,album=album,separator=globaldata.separator)
        counter=albummovie.movies.count()
        already_in_album=albummovie.movies.all()


    count=movies.count()
    items_per_page = 20 # Adjust this to your preferred value

    # Create a Paginator object with the movies queryset
    paginator = Paginator(movies, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    movies = paginator.get_page(page_number)

    li=[]

    #type checker is used to check for scene in index page
    typeChecker=False
    if album.type=="Scene":
        typeChecker=True
    if request.user.is_authenticated:
        user=request.user
        cart_item=Cartitem.objects.filter(user=user)



        for item in cart_item:
                li.append(item.product)

        for item in previous_movies_in_albums_bought:
                for itemdata in item:
                    li.append(itemdata)
        previous_items=Order_Product.objects.filter(user=user)
    
        for item in previous_items:
            li.append(item.product)


        context={

            'product':album,
            'movies':movies,
            'already_in_album':already_in_album,
            'itemsincart':li,
            # 'counter':album.counter,
            'counter':counter,
            'all_products':movies,
            'typeChecker':typeChecker,
            'count':count
        }
    else:
        context={
             'product':album,
            'movies':movies,
            'all_products':movies,
            'count':count
            

        }
    return render(request,"album-detail.html",context)


#everytime add to cart button is clicked this view is run which adds the particular movie to albummovie based on separator
def inc_counter(request,album_id,movie_id):
  album=Albums.objects.get(id=album_id)
  movie=MovieDetail.objects.get(id=movie_id)
  globaldata=Separator.objects.get(user=request.user)  #used so user can buy same album again and again
  album_movie,created=AlbumMovie.objects.get_or_create(user=request.user,album=album,separator=globaldata.separator)
  album_movie.movies.add(movie)
  album_movie.counter=album_movie.movies.count()
  album_movie.save()
  data = {
        'status': 'success',
        'count':album_movie.counter,
    }
  return JsonResponse(data)


#To remove the movie from package 
def dec_counter(request,album_id,movie_id):
  album=Albums.objects.get(id=album_id)
  movie=MovieDetail.objects.get(id=movie_id)
  globaldata=Separator.objects.get(user=request.user)
  album_movie=AlbumMovie.objects.get(user=request.user,album=album,separator=globaldata.separator)
  album_movie.movies.remove(movie)

  
  album_movie.save()
  data = {
        'status': 'success'
    }
  return JsonResponse(data)


#To create a dropdown in cart page
def get_movies_in_album(request,album_id):
    album=Albums.objects.get(id=album_id)
    globaldata=Separator.objects.get(user=request.user)
    albummovie=AlbumMovie.objects.get(user=request.user,album=album,separator=globaldata.separator)

    movie_data_list = []
    # Iterate through the movies and construct the full image URL for each
    for movie in albummovie.movies.all():
        if movie.coverphoto:
            coverphoto_url = request.build_absolute_uri(movie.coverphoto.url)
        else:
            coverphoto_url = None

        movie_data = {
            'movie_name': movie.movie_name,
            'coverphoto': coverphoto_url,
            # Add other movie data as needed
        }

        # Append the movie data to the list
        movie_data_list.append(movie_data)


    return JsonResponse({'status':"true","movies":movie_data_list})