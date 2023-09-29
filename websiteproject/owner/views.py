from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from indexapp.models import MovieDetail,ImagesModel,StarsModel,StudioModel
from albums.models import Albums
from django. contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from detailapp.models import Payment 
from django.db.models import Sum
# from .models import Product  # Replace `.models` with the actual path to your model
from datetime import datetime, timedelta

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
      total_price =Payment.objects.aggregate(total_price=Sum('amount_paid'))
      sum_of_prices = total_price['total_price']
      
      context={
        'get_data':get_data,
        'top_movie':top_movie,
        'latest_movie':latest_movie,
        'latest_user':latest_user,
        'total_price':sum_of_prices
      }

      return render(request,'owner/index.html',context)

  except PermissionDenied:
        return HttpResponse('Page not found')




@user_passes_test(is_superadmin)
def  add_item(request):
    star=StarsModel.objects.all().order_by('-id')
    studio=StudioModel.objects.all().order_by('-id')
    context={
      'star':star,
      'studio':studio,
    }
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
      if 'movie' in request.FILES:

        movie=request.FILES['movie']
      else:
        movie=None

      studioname=request.POST['studio']
     
      studio=StudioModel.objects.get(id=studioname)
      form=MovieDetail.objects.create(movie_name=title,studio=studio,year=releasedyear,type=type,quality=quality,coverphoto=cover_image,duration=length,short_description=text,trailer=movie,price=price)
      
      for uploaded_file in request.FILES.getlist('image'):
        image_instance=ImagesModel.objects.create(image=uploaded_file)
        images_list.append(image_instance)


      form.images.set(images_list)


      for star in request.POST.getlist('stars'):
        star=StarsModel.objects.get(id=star)
        form.stars.add(star)

      for gen in request.POST.getlist('genre'):
        category,created=Category.objects.get_or_create(category_name=gen)
        form.genre.add(category)


      form.save()
      messages.error(request,'please check a details')
      return render(request,'owner/add-item.html',context)
    return render(request,'owner/add-item.html',context)

  
  
@user_passes_test(is_superadmin)
def add_album(request):
   if request.method=="POST" and request.FILES.get('form__img-upload'):
      coverphoto=request.FILES['form__img-upload']
      title=request.POST['title']
      limit=request.POST['limit']
      price=request.POST['price']
      creator=Albums.objects.create(coverphoto=coverphoto,album_name=title,limit=limit,price=price,counter=0)
      for gen in request.POST.getlist('genre'):

        category,created=Category.objects.get_or_create(category_name=gen)
        creator.genre.add(category)

      
      creator.save()

   movies=MovieDetail.objects.all()
   context={
      'movies':movies
   }
   return render(request,"owner/add-album.html",context)
   





@user_passes_test(is_superadmin)
def catalog(request):
    movie_details=MovieDetail.objects.all().order_by('-id')
    count=movie_details.count()
    paginator=Paginator(movie_details,10)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    context={
      'item':paged_products,
      'all_products':paged_products,
      'count':count
    }
    return render(request,'owner/catalog.html',context)


@user_passes_test(is_superadmin)
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







@user_passes_test(is_superadmin)
def remove_movie(request,id):
  movie=MovieDetail.objects.get(id=id)
  movie.stars.clear()
  movie.genre.clear()
  movie.images.clear()
  movie.delete()
  return redirect('catalog')
 









def edit_user(request):
    return render(request,"owner/edit-user.html")


def user_list(request):
    userlist=Account.objects.all().order_by('-id')
    payment=Payment.objects.all().order_by('-id')
    count=userlist.count()
    paginator=Paginator(userlist,2)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)  
    user_totals = {}
    
    # Calculate the total amount paid by each user
    for payment_record in payment:
        user = payment_record.user
        amount_paid = payment_record.amount_paid
        if user in user_totals:
            user_totals[user]['total_paid'] += amount_paid
        else:
            user_totals[user] = {'user': user, 'total_paid': amount_paid}

    user_totals_list = user_totals.values()
    context={
'users': paged_products,
'count':count,
 'user_totals_list': user_totals_list,
 'all_products':paged_products
    }

    return render(request, 'owner/users.html', context)



@user_passes_test(is_superadmin)
def add_studio(request):
  if request.method == 'POST' :
    
      studioname=request.POST['studio']
      
     
      studio,created=StudioModel.objects.get_or_create(name=studioname.title())
      return render(request,'owner/add_studio.html')
  return render(request,'owner/add_studio.html')



@user_passes_test(is_superadmin)
def add_stars(request):
  if request.method == 'POST' :
      
      
      starimage=request.FILES['starimage']
      starname=request.POST['starname']
      starheight=request.POST['starheight']
      starhaircolor=request.POST['starhaircolor']
      starage=request.POST['starage']
      
      star,created=StarsModel.objects.get_or_create(name=starname.title(),height=starheight,haircolor=starhaircolor.title(),age=starage,image=starimage)
      
      

      return render(request,'owner/add_stars.html')
  return render(request,'owner/add_stars.html')




# def total_amount(request):
#   # payment=Payment.objects.all()
#   total_price =Payment.objects.aggregate(total_price=Sum('amount_paid'))
#   return render(request,'owner/index.html')

  

def show_transactions(request):
  if request.method=="POST":
    selected_time_range=request.POST['time_range']
    today = datetime.now().date()
    if selected_time_range == '1_month':
        start_date = today - timedelta(days=30)
    elif selected_time_range == '2_months':
        start_date = today - timedelta(days=60)
    elif selected_time_range == '3_months':
        start_date = today - timedelta(days=90)
    elif selected_time_range == '6_months':
        start_date = today - timedelta(days=180)
    elif selected_time_range == '1_week':
        start_date = today - timedelta(days=7)
    payments = Payment.objects.filter(created_at__gte=start_date).order_by('-id')

    return render(request, 'owner/transaction.html', {'payments': payments, 'selected_time_range': selected_time_range})




  payments=Payment.objects.all().order_by('-id')
  paginator=Paginator(payments,1)
  page=request.GET.get('page')
  paged_products=paginator.get_page(page)
  context={
    'payments':paged_products,
    'all_products':paged_products
  }

  return render(request,'owner/transaction.html',context)