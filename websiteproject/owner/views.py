from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from indexapp.models import MovieDetail,ImagesModel,StarsModel,StudioModel
from albums.models import Albums
from django. contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseNotFound

# from .forms import movie_form
from .forms import MovieDetailForm
from myaccount.models import Account
# Create your views here.
from category.models import Category
from django.contrib.auth.decorators import user_passes_test
def is_superadmin(user):
    return user.is_authenticated and user.is_superadmin

@user_passes_test(is_superadmin)
def dashboard(request):
  try:
      get_data=MovieDetail.objects.all().count()
      top_movie=MovieDetail.objects.all().order_by()[:5]
      latest_movie=MovieDetail.objects.all().order_by('-id')[:5]
      latest_user=Account.objects.all().order_by('-id')[:5]
      
      context={
        'get_data':get_data,
        'top_movie':top_movie,
        'latest_movie':latest_movie,
        'latest_user':latest_user,
      }

      return render(request,'owner/index.html',context)

  except PermissionDenied:
        return HttpResponse('Page not found')




def  add_item(request):
    
    if request.method == 'POST' and request.FILES.get('form__img-upload'):
      images_list=[]
      
      cover_image=request.FILES['form__img-upload']
      title=request.POST['title']
      text=request.POST['text']
      releasedyear=request.POST['releasedyear']
      length=request.POST['length']
      quality=request.POST['quality']
      type=request.POST['type']
      price=request.POST['price']
      movie=request.FILES['movie']
      starimage=request.FILES['starimage']
      starname=request.POST['starname']
      starheight=request.POST['starheight']
      starhaircolor=request.POST['starhaircolor']
      starage=request.POST['starage']
      studioname=request.POST['studio']
      
      star,created=StarsModel.objects.get_or_create(name=starname.title())
      
      star.height=starheight
      star.haircolor=starhaircolor
      star.age=starage
      star.image=starimage
      star.save()
      studio,created=StudioModel.objects.get_or_create(name=studioname.title())
      form=MovieDetail.objects.create(movie_name=title,studio=studio,year=releasedyear,type=type,quality=quality,coverphoto=cover_image,duration=length,short_description=text,trailer=movie,price=price)
      form.images.clear()
      form.genre.clear()
      form.stars.add(star)
      for uploaded_file in request.FILES.getlist('image'):
        image_instance=ImagesModel.objects.create(image=uploaded_file)
        images_list.append(image_instance)


      form.images.set(images_list)

      for gen in request.POST.getlist('genre'):
        category,created=Category.objects.get_or_create(category_name=gen)
        form.genre.add(category)


      form.save()
      messages.error(request,'please check a details')
      return render(request,'owner/add-item.html')
    return render(request,'owner/add-item.html')

  
  
def add_album(request):
   if request.method=="POST" and request.FILES.get('form__img-upload'):
      coverphoto=request.FILES['form__img-upload']
      title=request.POST['title']
      limit=request.POST['limit']
      price=request.POST['price']
      creator=Albums.objects.create(coverphoto=coverphoto,album_name=title,limit=limit,price=price,counter=0)

      
      creator.save()

   movies=MovieDetail.objects.all()
   context={
      'movies':movies
   }
   return render(request,"owner/add-album.html",context)
   





def catalog(request):
    movie_details=MovieDetail.objects.all().order_by('-id')
    # category=movie_details.genre.all()
    context={
      'item':movie_details
    }
    return render(request,'owner/catalog.html',context)


def edit_movie(request,id):
    movie = get_object_or_404(MovieDetail, pk=id)
    if request.method == 'POST':
        form = MovieDetailForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            print('hello world')
            form.save()
            return redirect('catalog')  # Redirect to the movie detail page after editing
        else:
          print(form.errors)
    else:
        form = MovieDetailForm(instance=movie)

    context = {
        'form': form,
        'movie': movie,
    }

    return render(request, 'owner/editmovie.html', context)







def remove_movie(request,id):
  print('hello world')
  movie=MovieDetail.objects.get(id=id)
  movie.delete()
  return redirect('catalog')
 









def edit_user(request):
    return render(request,"owner/edit-user.html")

def comments_list(request):
    return render(request,'owner/comments.html')

def user_list(request):
    return render(request,'owner/users.html')

