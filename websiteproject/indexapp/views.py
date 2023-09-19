from django.shortcuts import render
from .models import MovieDetail
# Create your views here.


def home(request):
    get_data=MovieDetail.objects.all()
    context={
        'get_data':get_data
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
