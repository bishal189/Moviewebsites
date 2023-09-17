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
    return render(request,'search.html')