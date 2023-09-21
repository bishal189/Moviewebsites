from django.shortcuts import render,get_object_or_404
from .models import MovieDetail
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
    
    # count1=paged_products.count()
    context={
        'all_products':paged_products,
        'get_data':all_product,
        'count':count,
        'allalbums':allalbums,
        
    }
    return render(request,'index.html',context)
    

def search(request):

    tosearch=request.POST['searchtext']
    print("search",tosearch)
    get_searched_data=MovieDetail.objects.filter(movie_name__icontains=tosearch)
    print(get_searched_data)
    context={
        'data':get_searched_data
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
