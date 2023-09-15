from django.shortcuts import render

# Create your views here.



def dashboard(request):
    return render(request,'owner/index.html')



def  add_item(request):
    return render(request,'owner/add-item.html')