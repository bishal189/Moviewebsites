from django.shortcuts import render,HttpResponse,redirect
from .forms import ResitrationForm
from.models import Account
from django.contrib import messages,auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
        print(user)
        if user is not None:  
            if Account.objects.filter(email=email,is_superadmin=True).exists():
                auth.login(request,user)
                return redirect('dashboard')
            else:    
               auth.login(request,user)
               return redirect('home')

        else:
            messages.error(request,'login credintials errors!')
            return redirect('login')    

    else:
        return render(request,'signin.html')    



# logout function is here 
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out!')
    return redirect('login')




def forget_password(request):
    if request.method == 'POST':
        email=request.POST['email']
        try:
          user=Account.objects.get(email=email)

        except:
            messages.error(request,'invalid email id,check it!')  
        print(user)


         # Generate the token for password reset or confirmation
        token = default_token_generator.make_token(user)
    
        # Encode the user's ID and token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = urlsafe_base64_encode(force_bytes(token))
    
     # Build the confirmation URL
        confirmation_url = reverse('password_confirmation', args=[uidb64, token])
    
        # Send the email with the confirmation URL
        subject = 'Confirm Your Account'
        message = f'Click the link below to confirm your account: {request.build_absolute_uri(confirmation_url)}'
        from_email = 'bishalmurmu150@gmail.com'
        recipient_list = [user.email]
    
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        # subject = 'Welcome to My Website'
        # message = 'Thank you for signing up for our website. please click to this link to reset your password http://localhost:8000/myaccounts/reset/ '
        # from_email = 'bishalmurmu150@gmail.com'  # Use your email address
        # recipient_list = [email]  # Replace with the recipient's email address
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return render(request,'forgot.html')







# User = get_user_model()

# # def password_confirmation(request, uidb64, token):
   

   

# def reset(request,uid64,token):
#     try:
#         # Decode the UID and get the user
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)

#         # Check if the token is valid
#         if default_token_generator.check_token(user, token):
#             # Token is valid, handle password reset here
#             # For example, render a password reset form
#             return render(request, 'password_confirmation.html', {'user': user})
#         else:
#             messages.error(request, 'Invalid confirmation link.')
#             return redirect('login')  # Redirect to login or an error page
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     # Handle invalid link or user not found here
#     messages.error(request, 'Invalid confirmation link.')
#     return redirect('login')  # Redirect to login or an error page
        
#     return render(request,'reset.html')
