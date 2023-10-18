from django.shortcuts import render
from .models import Contact
from django.contrib import messages
from owner.models import Page

# Create your views here.
#Simple contact view  simply stores data in db 
def contact(request):
    pages=Page.objects.all().order_by('-id')
    if request.method=='POST':
       print(request.POST)
       first_name=request.POST['first_name']
       last_name=request.POST['last_name']
       email=request.POST['email']
       subject=request.POST['subject']
       message=request.POST['text']
       contact_details=Contact(first_name=first_name,last_name=last_name,email=email,message=message,subject=subject)
       contact_details.save()
       messages.success(request,'Thanks You For Your Message')
       return render(request,'contacts.html',{'pages':pages})
    else:

        return render(request,'contacts.html',{'pages':pages})




