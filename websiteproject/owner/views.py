from django.shortcuts import render

# Create your views here.



def dashboard(request):
    return render(request,'owner/index.html')



def  add_item(request):
    return render(request,'owner/add-item.html')


def catalog(request):
    return render(request,'owner/catalog.html')

def edit_user(request):
    return render(request,"owner/edit-user.html")

def comments_list(request):
    return render(request,'owner/comments.html')

def user_list(request):
    return render(request,'owner/users.html')
