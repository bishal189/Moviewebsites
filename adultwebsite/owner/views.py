from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from indexapp.models import MovieDetail,ImagesModel,StarsModel,StudioModel
from albums.models import Albums
from django. contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from detailapp.models import Payment ,Order,Order_Product
from django.db.models import Sum,Count
from datetime import datetime, timedelta
from .models import Page
from .forms import MovieDetailForm
from myaccount.models import Account
from category.models import Category
from django.contrib.auth.decorators import user_passes_test
from indexapp.models import StarsModel


def is_superadmin(user):
    return user.is_authenticated and user.is_superadmin

@user_passes_test(is_superadmin)
def dashboard(request):
  try:
      get_data=MovieDetail.objects.all().count()
      top_movie=MovieDetail.objects.all().order_by('-cart_count','-view_count','-id')[:5]
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

#Adding new item from admin page
@user_passes_test(is_superadmin)
def  add_item(request):
    star=StarsModel.objects.all().order_by('-id')
    studio_en=StudioModel.objects.filter(lang='en').order_by('-id')
    genres_en=Category.objects.filter(lang='en').order_by('-id')

    studio_de=StudioModel.objects.filter(lang='de').order_by('-id')
    genres_de=Category.objects.filter(lang='de').order_by('-id')
    context={
      'star':star,
      'studio_en':studio_en,
      'genres_en':genres_en,
      'studio_de':studio_de,
      'genres_de':genres_de,
    }
    if request.method == 'POST' and request.FILES.get('form__img-upload'):
      images_list=[]
      
      cover_image=request.FILES['form__img-upload']
      title_en=request.POST['title_en']
      title_de=request.POST['title_de']
      text_en=request.POST['text_en']
      text_de=request.POST['text_de']
      videoname=request.POST['videoname']

      releasedyear=request.POST['releasedyear']
      length=request.POST['length']
      quality=request.POST['quality']
      type=request.POST['type']
      price=request.POST['price']

      if 'movie' in request.FILES:
        movie=request.FILES['movie']
      else:
        movie=None  

      form_en=MovieDetail.objects.create(movie_name=title_en,lang='en',videoname=videoname,year=releasedyear,type=type,quality=quality,coverphoto=cover_image,duration=length,short_description=text_en,trailer=movie,price=price)
      for uploaded_file in request.FILES.getlist('image'):
        image_instance=ImagesModel.objects.create(image=uploaded_file)
        images_list.append(image_instance)
      form_en.images.set(images_list)

      for star in request.POST.getlist('stars'):
        star=StarsModel.objects.get(id=star)
        form_en.stars.add(star)

      for studio in request.POST.getlist('studio_en'):
        studio=StudioModel.objects.get(id=studio)
        
      form_en.studio=studio
      for gen in request.POST.getlist('genre_en'):
        category=Category.objects.get(id=gen)
        form_en.genre.add(category)
      form_en.save()


      form_de=MovieDetail.objects.create(movie_name=title_de,lang='de',year=releasedyear,videoname=videoname,type=type,quality=quality,coverphoto=form_en.coverphoto,duration=length,short_description=text_de,trailer=form_en.trailer,price=price)
      

      form_de.images.set(images_list)

      for star in request.POST.getlist('stars'):
        star=StarsModel.objects.get(id=star)
        form_de.stars.add(star)

      for studio in request.POST.getlist('studio_de'):
        studio=StudioModel.objects.get(id=studio)
        
      form_de.studio=studio
      for gen in request.POST.getlist('genre_de'):
        category=Category.objects.get(id=gen)
        form_de.genre.add(category)
      form_de.save()



      messages.error(request,'please check a details')
      return render(request,'owner/add-item.html',context)
    return render(request,'owner/add-item.html',context)

  
  
@user_passes_test(is_superadmin)
def add_album(request):
   if request.method=="POST" and request.FILES.get('form__img-upload'):
      coverphoto=request.FILES['form__img-upload']
      title_en=request.POST['title_en']
      title_de=request.POST['title_de']
      limit=request.POST['limit']
      price=request.POST['price']
      type=request.POST['type']

      creator_en=Albums.objects.create(coverphoto=coverphoto,album_name=title_en,type=type,limit=limit,price=price,lang='en')
      for gen in request.POST.getlist('genre_en'):
        category=Category.objects.get(id=gen)
        creator_en.genre.add(category)     
      creator_en.save()


      creator_de=Albums.objects.create(coverphoto=creator_en.coverphoto,album_name=title_de,type=type,limit=limit,price=price,lang='de')
      for gen in request.POST.getlist('genre_de'):
        category=Category.objects.get(id=gen)
        creator_de.genre.add(category)     
      creator_de.save()

   genres_en=Category.objects.filter(lang='en').order_by('-id')
   genres_de=Category.objects.filter(lang='de').order_by('-id')

   context={
      'genres_en':genres_en,
      'genres_de':genres_de,
   }
   return render(request,"owner/add-album.html",context)
   

@user_passes_test(is_superadmin)
def catalog(request):
    if request.method=="POST":
       type=request.POST['type']
       toSearch=None
       if request.POST['toSearch']:
          toSearch=request.POST['toSearch']

       if type=="videos":
           if toSearch is not None:
              movie_details=MovieDetail.objects.filter(movie_name__icontains=toSearch).order_by('-id')
           else:
              movie_details=MovieDetail.objects.all().order_by('-id')

           count=movie_details.count()
           paginator=Paginator(movie_details,10)
           page=request.GET.get('page')
           paged_products=paginator.get_page(page)
           context={
            'item':paged_products,
            'all_products':paged_products,
            'count':count,
            'selected':type
           }
           return render(request,'owner/catalog.html',context)
       if type=="albums":
          if toSearch is not None:
             albums=Albums.objects.filter(album_name__icontains=toSearch).order_by('-id')
          else:
             
            albums=Albums.objects.all().order_by('-id')
          count=albums.count()
          paginator=Paginator(albums,10)
          page=request.GET.get('page')
          paged_products=paginator.get_page(page)
          context={
            'item':paged_products,
            'all_products':paged_products,
            'count':count,
            'selected':type
           }
          return render(request,'owner/catalog.html',context)
          
          
    movie_details=MovieDetail.objects.all().order_by('-id')
    count=movie_details.count()
    paginator=Paginator(movie_details,10)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    context={
      'item':paged_products,
      'all_products':paged_products,
      'count':count,
      'selected':"videos"
    }
    return render(request,'owner/catalog.html',context)


@user_passes_test(is_superadmin)
def edit_movie(request,id):
    movie = get_object_or_404(MovieDetail, pk=id)
    genres=Category.objects.all().order_by('-id')
    types=MovieDetail.objects.all().order_by('-id')
    print(request.POST)

    if request.method == 'POST':
        form = MovieDetailForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            
            if not form.cleaned_data['images']:
              form.cleaned_data['images'] = movie.images.all()
            
            
            selected_genre = request.POST.get('genre_en')
            movie.type = selected_genre


            genre = request.POST.get('genre')
            if genre:
              for genre_id in genre:
                  genre = Category.objects.get(pk=genre_id)
                  movie.genre.add(genre)
            

            
          
            form.save()
            return redirect('catalog')  # Redirect to the movie detail page after editing
        else:
          print(form.errors)
    else:
        form = MovieDetailForm(instance=movie)

    context = {
        'types':types,
        'genres':genres,
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



@user_passes_test(is_superadmin)
def remove_album(request,id):
  movie=Albums.objects.get(id=id)
  movie.delete()
  return redirect('catalog')
 


@user_passes_test(is_superadmin)
def edit_user(request):
    return render(request,"owner/edit-user.html")

@user_passes_test(is_superadmin)
def user_list(request):
    if request.method=="POST":
      toSearch=request.POST['toSearch']
      print(toSearch)
      userlist=Account.objects.filter(username__icontains=toSearch).order_by('-id')

    else:
         
      userlist=Account.objects.all().order_by('-id')

    payment=Payment.objects.all().order_by('-id')
    count=userlist.count()
    paginator=Paginator(userlist,20)
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
      if 'studio_en' in request.POST and request.POST['studio_en']!="":
          studioname_en=request.POST['studio_en']
          studio,created=StudioModel.objects.get_or_create(name=studioname_en.title(),lang='en')

      if 'studio_de' in request.POST and request.POST['studio_de']!="":
         studioname_de=request.POST['studio_de']
         studio,created=StudioModel.objects.get_or_create(name=studioname_de.title(),lang='de')


      return render(request,'owner/add_studio.html')
  return render(request,'owner/add_studio.html')

@user_passes_test(is_superadmin)
def add_genre(request):
  if request.method == 'POST' :
      if 'genrename_en' in request.POST and request.POST['genrename_en']!="":
        genrename_en=request.POST['genrename_en']
        category,created=Category.objects.get_or_create(category_name=genrename_en.title(),lang='en')
      
      if 'genrename_de' in request.POST and request.POST['genrename_de']!="":
         genrename_de=request.POST['genrename_de']
         category,created=Category.objects.get_or_create(category_name=genrename_de.title(),lang='de')
         

      return render(request,'owner/add-genre.html')
  return render(request,'owner/add-genre.html')



@user_passes_test(is_superadmin)
def add_stars(request):
  if request.method == 'POST' :
      
      
      starimage=request.FILES['starimage']
      starname=request.POST['starname']
      starheight=request.POST['starheight']
      starhaircolor=request.POST['starhaircolor']
      starage=request.POST['starage']
      starbirthplace=request.POST['starbirthplace']
      starethnicity=request.POST['starethnicity']
      starnationality=request.POST['starnationality']
      starweight=request.POST['starweight']
      stareyecolor=request.POST['stareyecolor']
      starbodytype=request.POST['starbodytype']
      starpiercing=request.POST['starpiercing']
      startatoo=request.POST['startatoo']

      starbreastsize=request.POST['starbreastsize']
      starbreasttype=request.POST['starbreasttype']
      starbodymarking=request.POST['starbodymarking']
      starcurrentstatus=request.POST['starcurrentstatus']
      stargender=request.POST['stargender']
      starmodeltype=request.POST['starmodeltype']

      
      star = StarsModel.objects.create(
        name=starname.title(),
        height=float(starheight) if starheight else None,
        dob=starage if starage else None,
        image=starimage if starimage else None,
        birthplace=starbirthplace.title() if starbirthplace else None,
        nationality=starnationality.title() if starnationality else None,
        weight=int(starweight) if starweight else None,

        piercing=starpiercing.title() if starpiercing else None,
        tatoo=startatoo.title() if startatoo else None,
        ethnicity=starethnicity  if starethnicity and starethnicity!="" else None,
        haircolor=starhaircolor if starhaircolor and starhaircolor!="" else None,
        eyecolor=stareyecolor if stareyecolor and stareyecolor!="" else None,
        bodytype=starbodytype if starbodytype and starbodytype!="" else None,
        breastsize=starbreastsize if starbreastsize and starbreastsize!="" else None,
        breasttype=starbreasttype if starbreasttype and starbreasttype!="" else None,
        bodymarking=starbodymarking if starbodymarking and starbodymarking!="" else None,

        currentstatus=starcurrentstatus if starcurrentstatus and starcurrentstatus!="" else None,
        gender=stargender if stargender and stargender!="" else None,
        modeltype=starmodeltype if starmodeltype and starmodeltype!="" else None,

      )
      star.save()
      

      return render(request,'owner/add_stars.html')
  return render(request,'owner/add_stars.html')




# def total_amount(request):
#   # payment=Payment.objects.all()
#   total_price =Payment.objects.aggregate(total_price=Sum('amount_paid'))
#   return render(request,'owner/index.html')

  
@user_passes_test(is_superadmin)
def show_transactions(request):
  if request.method=="POST":
    payments=None
    context=None
    if request.POST['time_range']:

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
      paginator=Paginator(payments,20)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)

      context={
        'payments':paged_products,
        'selected_time_range':selected_time_range,
      }

    if request.POST['item_count']:
      item_count=request.POST['item_count']
      if payments is None:

        payments=Payment.objects.all().order_by('-id')

      paginator=Paginator(payments,item_count)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)

      if context is None:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count
    
      }
      else:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count,
        'selected_time_range':selected_time_range,    
        }

    return render(request, 'owner/transaction.html', context)


  payments=Payment.objects.all().order_by('-id')
  paginator=Paginator(payments,20)
  page=request.GET.get('page')
  paged_products=paginator.get_page(page)
  context={
    'payments':paged_products,
    'all_products':paged_products
  }

  return render(request,'owner/transaction.html',context)

@user_passes_test(is_superadmin)
def show_transactions_country(request):
  if request.method=="POST":
    payments=None
    context=None
    if request.POST['time_range']:
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

      orders_by_country = (
          Order.objects.filter(payment__in=payments)
                      .values('country')
                      .annotate(total_price=Sum('total'))
                      .annotate(total_count=Count('id'))
                      .order_by('country')
      )
      paginator=Paginator(orders_by_country,20)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)
      context={
      'payments':paged_products,
      'all_products':paged_products,
      'selected_time_range': selected_time_range
      }


    if request.POST['item_count']:
      item_count=request.POST['item_count']
      if payments is None:

        payments=Payment.objects.all().order_by('-id')

      orders_by_country = (
          Order.objects.filter(payment__in=payments)
                      .values('country')
                      .annotate(total_price=Sum('total'))
                      .annotate(total_count=Count('id'))
                      .order_by('country')
      )

      paginator=Paginator(orders_by_country,item_count)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)

      if context is None:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count
    
      }
      else:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count,
        'selected_time_range':selected_time_range,    
        }

    return render(request, 'owner/transaction-country.html',context)


  payments = Payment.objects.all()
  orders_by_country = (
        Order.objects.filter(payment__in=payments)
                    .values('country')
                    .annotate(total_price=Sum('total'))
                    .annotate(total_count=Count('id'))
                    .order_by('country')
    )
  paginator=Paginator(orders_by_country,20)
  page=request.GET.get('page')
  paged_products=paginator.get_page(page)
  context={
    'payments':paged_products,
    'all_products':paged_products
  }

  return render(request,'owner/transaction-country.html',context)

@user_passes_test(is_superadmin)
def show_transactions_product(request):
  if request.method=="POST":
    if request.method=="POST":
      payments=None
      context=None
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
      orders_by_product = (
          Order_Product.objects.filter(payment__in=payments)
                      .values('product__movie_name')
                      .annotate(total_price=Sum('product_price'))
                      .annotate(total_count=Count('id'))
                      .order_by('product__id')
                      .values('product__movie_name','total_price','total_count','product__view_count')
                      
      )
      paginator=Paginator(orders_by_product,20)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)
      context={
      'payments':paged_products,
      'all_products':paged_products,
      'selected_time_range': selected_time_range,
      }
    if request.POST['item_count'] != 20:
      item_count=request.POST['item_count']
      if payments is None:

        payments=Payment.objects.all().order_by('-id')

      orders_by_product = (
          Order_Product.objects.filter(payment__in=payments)
                      .values('product__movie_name')
                      .annotate(total_price=Sum('product_price'))
                      .annotate(total_count=Count('id'))
                      .order_by('product__id')
                      .values('product__movie_name','total_price','total_count','product__view_count')
                      
      )

      paginator=Paginator(orders_by_product,item_count)
      page=request.GET.get('page')
      paged_products=paginator.get_page(page)

      if context is None:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count
    
      }
      else:
        context={
        'payments':paged_products,
        'all_products':paged_products,
        'selected_item_count':item_count,
        'selected_time_range':selected_time_range,    
        }
      


    return render(request, 'owner/transaction-product.html',context )


  payments = Payment.objects.all()
  orders_by_product = (
        Order_Product.objects.filter(payment__in=payments)
                    .values('product__movie_name')
                    .annotate(total_price=Sum('product_price'))
                    .annotate(total_count=Count('id'))
                    .order_by('product__id')
                    .values('product__movie_name','total_price','total_count','product__view_count')
                    
    )
    
  paginator=Paginator(orders_by_product,20)
  page=request.GET.get('page')
  paged_products=paginator.get_page(page)
  context={
    'payments':paged_products,
    'all_products':paged_products
  }

  return render(request,'owner/transaction-product.html',context)





from .forms import Album_form
@user_passes_test(is_superadmin)
def edit_album(request,id):
    genres=Category.objects.all().order_by('-id')
    album = get_object_or_404(Albums, pk=id)
    if request.method == 'POST':
        form =Album_form(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            return redirect('catalog')  # Redirect to the movie detail page after editing
        else:
          print(form.errors)
    else:
        form = Album_form(instance=album)

    context = {
        'form': form,
        'movie': album,
        'genres':genres,
    }

    return render(request, 'owner/edit_album.html', context)




def delete_user(request,id):
  user=Account.objects.get(id=id)
  user.delete()
  return redirect('user_list')

def user_delete_user(request,id):
  user=Account.objects.get(id=id)
  user.delete()
  return redirect('home')



def suspended_user(request,id):

  user=Account.objects.get(id=id)
  if user is not None:
    user.is_suspended=True
    user.save()
    return redirect('user_list')
    
def active_user(request,id):

  user=Account.objects.get(id=id)
  if user is not None:
    user.is_suspended=False
    print(user)
    user.save()
    return redirect('user_list')
    



# for displaying all pages
@user_passes_test(is_superadmin)
def pages(request):
   all_pages=Page.objects.all()

   context={
      'all_pages':all_pages
   }
   return render(request,'owner/pages.html',context)

@user_passes_test(is_superadmin)
def add_page(request):

  if request.method=="POST":
      title_en=request.POST['title_en']
      status=request.POST['status']
      body_en=request.POST['body_en']
      title_de=request.POST['title_de']
      body_de=request.POST['body_de']
      
      pages_en=Page.objects.create(title=title_en,status=status,body=body_en,lang='en')
      pages_en.save()
      pages_de=Page.objects.create(title=title_de,status=status,body=body_de,lang='de')
      pages_de.save()

      all_pages=Page.objects.all()
   

      context={
      'all_pages':all_pages
        }
      return render(request,'owner/pages.html',context)
  return render(request,'owner/add-page.html')
def deactivate_page(request,id):
   page=Page.objects.get(id=id)
   page.status="Inactive"
   page.save()
   all_pages=Page.objects.all()
   

   context={
      'all_pages':all_pages
   }
   return render(request,'owner/pages.html',context)

   
def delete_page(request,id):
   page=Page.objects.get(id=id)
   page.delete()
   all_pages=Page.objects.all()

   context={
      'all_pages':all_pages
   }
   return render(request,'owner/pages.html',context)
   
@user_passes_test(is_superadmin)
def activate_page(request,id):
   page=Page.objects.get(id=id)
   page.status="Active"
   all_pages=Page.objects.all()
   page.save()
   context={
      'all_pages':all_pages
   }
   return render(request,'owner/pages.html',context)
@user_passes_test(is_superadmin)   
def edit_page(request,id):
   page=Page.objects.get(id=id)
   context={
      'page':page
   }
   if request.method=="POST":
      body=request.POST['body']
      title=request.POST['title']
      status=request.POST['status']

      page.body=body
      page.title=title
      page.status=status
      page.save()
      pages=Page.objects.all()
      context={
         'all_pages':pages
         }
      return render(request,'owner/pages.html',context)
   return render(request,'owner/edit-page.html',context)
   

@user_passes_test(is_superadmin)
def stars_catalog(request):
  get_stars=StarsModel.objects.all().order_by('-id')
  context={
    'stars':get_stars
  }
  return render(request,'owner/stars_catalog.html',context)


@user_passes_test(is_superadmin)
def edit_stars(request,id):
  stars= StarsModel.objects.get(id=id)
  
  if request.method == 'POST':
      starimage=None
      if 'starimage' in request.FILES:
        starimage=request.FILES['starimage']
      starname=request.POST['starname']
      starheight=request.POST['starheight']
      starhaircolor=request.POST['starhaircolor']
      starage=request.POST['starage']
      starbirthplace=request.POST['starbirthplace']
      starethnicity=request.POST['starethnicity']
      starnationality=request.POST['starnationality']
      starweight=request.POST['starweight']
      stareyecolor=request.POST['stareyecolor']
      starbodytype=request.POST['starbodytype']
      starpiercing=request.POST['starpiercing']
      startatoo=request.POST['startatoo']

      starbreastsize=request.POST['starbreastsize']
      starbreasttype=request.POST['starbreasttype']
      starbodymarking=request.POST['starbodymarking']
      starcurrentstatus=request.POST['starcurrentstatus']
      stargender=request.POST['stargender']
      starmodeltype=request.POST['starmodeltype']

      print(float(starheight))
      stars.name=starname.title()
      stars.height=float(starheight) if starheight else None
      # print(stars.height)
      stars.dob=starage if starage else None
      
      if starimage is not  None:
        stars.image=starimage
      stars.birthplace=starbirthplace.title() if starbirthplace else None
      stars.nationality=starnationality.title() if starnationality else None
      stars.weight=int(starweight) if starweight else None

      stars.piercing=starpiercing.title() if starpiercing else None
      stars.tatoo=startatoo.title() if startatoo else None
      stars.ethnicity=starethnicity  if starethnicity and starethnicity!="" else None
      stars.haircolor=starhaircolor if starhaircolor and starhaircolor!="" else None
      stars.eyecolor=stareyecolor if stareyecolor and stareyecolor!="" else None
      stars.bodytype=starbodytype if starbodytype and starbodytype!="" else None
      stars.breastsize=starbreastsize if starbreastsize and starbreastsize!="" else None
      stars.breasttype=starbreasttype if starbreasttype and starbreasttype!="" else None
      stars.bodymarking=starbodymarking if starbodymarking and starbodymarking!="" else None

      stars.currentstatus=starcurrentstatus if starcurrentstatus and starcurrentstatus!="" else None
      stars.gender=stargender if stargender and stargender!="" else None
      stars.modeltype=starmodeltype if starmodeltype and starmodeltype!="" else None

      
      stars.save()  
      get_stars=StarsModel.objects.all().order_by('-id')
      context={
      'stars':get_stars
       }
      return render(request,'owner/stars_catalog.html',context)

  context = {
        
        'star': stars,
    }

  return render(request, 'owner/edit_stars.html', context)
  





def delete_stars(reqeust,id):
  get_stars=get_object_or_404(StarsModel,id=id)
  get_stars.delete()
  return redirect('stars_catalog')

