from django.shortcuts import render,get_object_or_404
from .models import MovieDetail,StarsModel
from indexapp.models import Category
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
from albums.models import Albums

def home(request):
   
    all_product=MovieDetail.objects.all().order_by('id')
    paginator=Paginator(all_product,10)
    page=request.GET.get('page')
    paged_products=paginator.get_page(page)
    count=all_product.count()
    allalbums=Albums.objects.all()
    stardata=StarsModel.objects.all()
    genres=Category.objects.all()

    # count1=paged_products.count()
    context={
        'genres':genres,
        'all_products':paged_products,
        'get_data':all_product,
        'count':count,
        'allalbums':allalbums,
        'star':stardata,


        
    }
    return render(request,'index.html',context)
    

def search(request):
   
    tosearch=request.POST['searchtext']
    get_dvd=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="DVD")
    get_scene=MovieDetail.objects.filter(movie_name__icontains=tosearch,type="Scene")
   
    paginator = Paginator(get_dvd, per_page=1)
    paginator1=Paginator(get_scene,per_page=1)  # Set the number of items per page (e.g., 10 items per page)
    page_number = request.GET.get('page') 
    page_number1=request.GET.get('page') # Get the current page number from the request
    paged_products = paginator.get_page(page_number)  # Get the Page object for the current page
    paged_products1 = paginator1.get_page(page_number1)  # Get the Page object for the current page
    context={
        'data1':get_scene,
        'all_products':paged_products,
        'tosearch':tosearch,
        'all_products1':paged_products1
        
        
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



def scenes(request):
    alldata=MovieDetail.objects.filter(type='Scene')
    
    return render(request,'scenes.html',{'alldata':alldata})


def dvd(request):
    alldata=MovieDetail.objects.filter(type='DVD')
    return render(request,'dvd.html',{'alldata':alldata})

def stars(request):
    allstars=StarsModel.objects.all().order_by('-id')
    context={
        'stars':allstars,
    }
    return render(request,'stars.html',context)
def star_detail(request,id):
    star=StarsModel.objects.get(id=id)
    movies=MovieDetail.objects.filter(stars=star)
    print(star.name,movies)
    context={
        'star':star,
        'movies':movies,
    }
    return render(request,'stardetail.html',context)