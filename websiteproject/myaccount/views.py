from django.shortcuts import render,HttpResponse,redirect
from .forms import ResitrationForm
from.models import Account
from django.contrib import messages,auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.  
# 
# 
# 
# register page is here   
def Register(request):
    if request.method == 'POST':
        form =ResitrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']   
            email=form.cleaned_data['email']  
            password=form.cleaned_data['password']  
            username=email.split("@")[0]

            user=Account.objects.create_user(email=email,username=username,password=password )
            user.save()




            # user activation
            # current_site=get_current_site(request)
            # mail_subject='Please activate your account'
            # message=render_to_string('accounts/account_verfication_email.html',{
            #     'user':user,
            #     'domain':current_site,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':default_token_generator.make_token(user),
            # })
            # to_email=email
            # send_email=EmailMessage(mail_subject,message,to=[to_email])
            # send_email.send()







            
            messages.success(request,'Registration successful')
            return redirect('signup')




    else:
       form=ResitrationForm()
    context={ 
        'form':form
    }
    return render(request,'signup.html',context)







# the login function

def Login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        
        user=auth.authenticate(email=email,password=password)
        if request.user.is_superuser:
            return redirect('index_admin')
        if user is not None:
            auth.login(request,user)
            return redirect('home')

        else:
            messages.error(request,'invalid login credentials')   
            return redirect('/myaccounts/login') 

    else: 
      return render(request,'signin.html')





# logout function is here 
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out!')
    return redirect('login')
