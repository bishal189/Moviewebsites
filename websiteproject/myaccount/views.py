# Import your Account model or replace with the correct import
from .models import Account
from django.utils.encoding import force_str
import django
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, HttpResponse, redirect
from .forms import ResitrationForm
from .models import Account
from indexapp.models import FavouritesModel
from detailapp.models import Order_Product,Payment,Order
# from django.utils.encoding import force_text
from django.contrib import messages, auth
# verification email module import
# Create your views here.
#
django.utils.encoding.force_text = force_str
#
#
# register page is here


def Register(request):
    if request.method == 'POST':
        form = ResitrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = Account.objects.create_user(
                email=email, username=username, password=password)
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

            messages.success(request, 'Registration successful')
            return redirect('login')

    else:
       form = ResitrationForm()
    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


# the login function

def Login(request):
    url=request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_suspended:
            messages.error(request, 'You have been suspended by the admin!')
            return redirect('login')
        else:
            if user is not None:
                if Account.objects.filter(email=email, is_superadmin=True).exists():
                    auth.login(request, user)
                    return redirect('home')
                else:
                    auth.login(request, user)
                    return redirect('home')

            else:
                messages.error(request, 'login credintials errors!')
                return redirect('login')

    else:
        return render(request, 'signin.html')


# logout function is here
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out!')
    return redirect('home')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
        except :
            # Handle the case where the user does not exist
            return render(request, 'forgot.html', {'error_message': 'User does not exist'})

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.id))

        # Construct the password reset link
        current_site = get_current_site(request)
        reset_link = f"{current_site}/myaccounts/password_validate/{uid}/{token}"
        subject = 'Password Reset'
        message = f'Click the following link to reset your password:\n\n{reset_link}'

        # Send the email
        send_mail(subject, message, 'bishalmurmu150@gmail.com', [email])

        # Redirect to a success page or display a message
        return render(request, 'reset.html')


    else:
        return render(request,'forgot.html')


        # Use the 'username' value here
    

def reset_password_validate(request,uidb64,token):
    print('hello','*******************')
    # validate the user by decoding the token and user primary key
    try:
        uid=urlsafe_base64_decode(uidb64).decode() 
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,user.DoesNotExist):
        user=None
     
    if user is not None and default_token_generator.check_token(user,token):

        request.session['uid']=uid
        print(uid)
        print(request.session.get('uid'))
        messages.info(request,'please reset your password')
        context={
            'uid':uid,
        }
        return render(request,'reset.html',context)
    else:
        messages.error(request,'this link has been expired.')
        return redirect('forgot')


# def forget_password(request):
#     if request.method == 'POST':
#         email=request.POST['email']
#         try:
#             user=Account.objects.get(email=email)
#         # user activation
#             current_site=get_current_site(request)
#             mail_subject='Please reset your account'
#             message=render_to_string('reset/reset.html',{
#                 'user':user,
#                 'domain':current_site,
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token':default_token_generator.make_token(user),
#             })
#             to_email=email
#             send_email=EmailMessage(mail_subject,message,to=[to_email])
#             send_email.send()
#         except:
#             messages.error(request,'no email matches!')
#             return render(request,'forgot.html')

#     return render(request,'forgot.html')    
    




def reset_password(request):
    if request.method == 'POST':
        password= request.POST['password']
        id= request.POST['id']
        confirm_password= request.POST['new_password']
        if  password == confirm_password:
            print('anotherpage')
           
            # pk=request.session.get('uid')
          
            user=Account.objects.get(pk=id)
            print(user)
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'password reset sucessful')
            return render(request,'signin.html')
        else:
            messages.error(request,'password does not match')
            return render(request,'reset.html')
  
    return render(request,'reset.html')
















def profile(request):
    orders=Order_Product.objects.filter(user=request.user)
    payments=Payment.objects.filter(user=request.user).order_by('-id')
    try:
        favourites=FavouritesModel.objects.get(user=request.user)
    except:
        favourites=None
    orders_product = Order.objects.filter(payment__in=payments).order_by('-id')
    print(favourites)
    return render(request,'profile.html',{'orders':orders,'favourites':favourites,'orders_product':orders_product})



def changed_password(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        confrim_password=request.POST['new_password']
        if password==confrim_password:
            user=Account.objects.get(email=email)
            user.set_password(password)
            user.save()
            print('done')
            return redirect('profile')
        else:
            return messages.error(request,'password doesnot match')


