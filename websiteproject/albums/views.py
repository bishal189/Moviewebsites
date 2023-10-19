from django.shortcuts import render
from indexapp.models import MovieDetail
from .models import Albums,AlbumMovie,Separator
from django.http import JsonResponse
from django.core.paginator import Paginator
from detailapp.models import Cartitem,Order_Product_album,Order_Product
from django.template.loader import render_to_string
from owner.models import Page
#for getting the list of albums in album page
def album(request):
    pages=Page.objects.all().order_by('-id')
    albums=Albums.objects.filter(lang=request.LANGUAGE_CODE).order_by('-id')
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
        'albums':paged_album,
        'pages':pages,
    }
    return render(request,'album.html',context)



#for getting the particular album besed on id
def album_detail(request,id):
    pages=Page.objects.all().order_by('-id')
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
        
        #movies already bought are not shown album 
        filtered_movie_details = [movie for movie in movies if movie not in li]    
        paginator = Paginator(filtered_movie_details, 20)

    # Get the current page number from the request's GET parameters
        page_number = request.GET.get('page_album')

    # Get the Page object for the current page
        paged_data = paginator.get_page(page_number)
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'Fetch':
            response_data=None
            page_album=request.GET.get('page_album')

            if page_album is not None:
                paged_album= paginator.get_page(page_album)
                album_html = render_to_string('partial/album_detail_partial.html', {'product':album,'movies': paged_album}, request=request)
                pagination_html = render_to_string('partial/pagination_partial.html', {'data': paged_album,'type':"album",}, request=request)
                response_data = {
            'content': album_html,
            'pagination': pagination_html,
                }
            return JsonResponse(response_data)
        
        
        context={

            'product':album,
            'movies':paged_data,
            'already_in_album':already_in_album,
            'counter':counter,
            'typeChecker':typeChecker,
            'count':count,
            'pages':pages
        }
    else:
        context={
             'product':album,
            'movies':movies,
            'count':count,
            'pages':pages,

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