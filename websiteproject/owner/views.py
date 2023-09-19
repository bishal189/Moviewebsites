from django.shortcuts import render
from indexapp.models import MovieDetail,ImagesModel
from django. contrib import messages
from .forms import movie_form
# Create your views here.
from category.models import Category


def dashboard(request):
  return render(request,'owner/index.html')



def  add_item(request):
    
    if request.method == 'POST' and request.FILES.get('form__img-upload'):
      images_list=[]
      print(request.POST)
      cover_image=request.FILES['form__img-upload']
      title=request.POST['title']
      text=request.POST['text']
      releasedyear=request.POST['releasedyear']
      length=request.POST['length']
      quality=request.POST['quality']
      price=request.POST['price']
      movie=request.FILES['movie']
      link=request.POST['link']
      form=MovieDetail.objects.create(movie_name=title,year=releasedyear,quality=quality,coverphoto=cover_image,duration=length,short_description=text,trailer=movie,price=price,link=link)
      form.images.clear()
      form.genre.clear()
      for uploaded_file in request.FILES.getlist('image'):
        image_instance=ImagesModel.objects.create(image=uploaded_file)
        images_list.append(image_instance)


      form.images.set(images_list)

      for gen in request.POST.getlist('genre'):
        print(gen)
        category,created=Category.objects.get_or_create(category_name=gen)
        form.genre.add(category)


      form.save()
      messages.error(request,'please check a details')
      return render(request,'owner/add-item.html')
    return render(request,'owner/add-item.html')

  


def catalog(request):
    return render(request,'owner/catalog.html')

def edit_user(request):
    return render(request,"owner/edit-user.html")

def comments_list(request):
    return render(request,'owner/comments.html')

def user_list(request):
    return render(request,'owner/users.html')

