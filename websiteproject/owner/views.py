from django.shortcuts import render
from indexapp.models import MovieDetail
from django. contrib import messages
from .forms import movie_form
# Create your views here.



def dashboard(request):
  return render(request,'owner/index.html')



def  add_item(request):

    if request.method == 'POST':
      cover_image=request.POST['form__img-upload']
      title=request.POST['title']
      text=request.POST['text']
      releasedyear=request.POST['releasedyear']
      length=request.POST['length']
      quality=request.POST['quality']
      price=request.POST['price']
      genere=request.POST['genere']
      image=request.POST['image']
      movie=request.POST['movie']
      link=request.POST['link']
      form=MovieDetail.objects.create(movie_name=title,year=releasedyear,quality=quality,coverphoto=cover_image,duration=length,short_description=text,thumbnail=image,trailer=movie,price=price,link=link)
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

