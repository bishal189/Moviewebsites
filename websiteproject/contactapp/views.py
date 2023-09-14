from django.shortcuts import render
from .models import Contact
from django.contrib import messages,auth

# Create your views here.

def contact(request):
    if request.method=='POST':
       print(request.POST)
       first_name=request.POST['first_name']
       last_name=request.POST['last_name']
       email=request.POST['email']
       subject=request.POST['subject']
       message=request.POST['text']
       contact_details=Contact(first_name=first_name,last_name=last_name,email=email,message=message,subject=subject)
       contact_details.save()
       messages.success(request,'You have contact us! Thanks You')
       return render(request,'contacts.html')
    else:

        return render(request,'contacts.html')




