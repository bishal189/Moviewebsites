from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Album_item, Albums,Order_Product_album
from .models import Cart,Cartitem
from indexapp.models import MovieDetail
from albums.models import Albums,AlbumMovie,Separator
from .models import Album_item
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .forms import Order,OrderForm
from .models import Order,Order_Product,Payment
import json
from django.http import JsonResponse,HttpResponse
import datetime
from django.template import loader
import pdfkit
from itertools import chain
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart   

def details(request,slug=None):
    product =MovieDetail.objects.get(slug=slug)
    product.view_count=product.view_count+1
    product.save()
    user=request.user
    newmovies=MovieDetail.objects.all().order_by('-id')[:5]
    similar=MovieDetail.objects.all().order_by('?')[:20]
    li=[]
    if request.user.is_authenticated:

        cart_item=Cartitem.objects.filter(user=user)

        for item in cart_item:
                li.append(item.product)
        
        val=product in li

        order_item=Order_Product.objects.filter(user=user)
        order_li=[]
        for item in order_item:
            order_li.append(item.product)

        print(order_li,product,"a")
        already_bought=product in order_li
        print(already_bought)
        context={
            'val':val,
            'already_bought':already_bought,
            'product':product,
            'notlogin':False,
            'newmovies':newmovies,
            'similar':similar,
        }
        
        return render(request,'details.html',context)
    else:
       product =MovieDetail.objects.get(slug=slug)
       context={
            'val':False,
            'product':product,
            'notlogin':True,
            'newmovies':newmovies,
            'similar':similar,
        }
       return render(request,'details.html',context)


def remove_album(request,album_id):
    allcartitems=Cartitem.objects.all()
    allcartitems.delete()
    albums=Albums.objects.get(id=album_id)
    albums.movies.clear()
    albums.counter=0
    albums.save()
    

    return redirect('cart')



def add_cart(request,product_id,album_price=None):
    # if the user is login 
    current_user=request.user
     
    product=MovieDetail.objects.get(id=product_id) #get the particular product
    product.cart_count=product.cart_count+1
    product.save()
    if current_user.is_authenticated:
        product_variation=[]
        if request.method == "POST":
            for item in request.POST:
                key=item;
                value=request.POST[key]
                
                # try:
                #     variation=Variation.objects.get(variation_category__iexact=key,variation_value__iexact=value)
                #     # print(variation)
                #     product_variation.append(variation)
                # except:
                #     pass    
            

        # now add the product in the cart   

        is_cart_item_exist=Cartitem.objects.filter(product=product,user=current_user).exists()

        if is_cart_item_exist:
            cart_item=Cartitem.objects.filter(product=product,user=current_user)

            # if that product exist than which variation exist of that product
            # checking the variation of the quantity



            # we need three things

            #existiong variation->from database
            #current variation_->from product variation
            #item_id->database
            ex_var_list=[]
            id=[]
            for item in cart_item:
                # existing_variation=item.variations.all()
                # ex_var_list.append(list(existing_variation))
                id.append(item.id)

            # print(ex_var_list)
            if product_variation in ex_var_list:
            #   increase the cart item quantity
                index=ex_var_list.index(product_variation)
                
                item_id=id[index]
                
            

                item=Cartitem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()

            else:
                
                item=Cartitem.objects.create(product=product,quantity=1,user=current_user)
                if(len(product_variation))>0:
                    
                  item.variations.clear()
                  item.variations.add(*product_variation)
                item.save()    
            
            
    



        
        
            # cart_item.quantity=cart_item.quantity+1;
            

        else :

            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                user=current_user
            )
            if(len(product_variation))>0:
              cart_item.variations.clear()
              cart_item.variations.add(*product_variation)

            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        return redirect('cart');   
    else:
        # if the user is not login
        product_variation=[]
        if request.method == "POST":
            for item in request.POST:
                key=item;
                value=request.POST[key]
                
                try:
                    pass
                    # variation=Variation.objects.get(variation_category__iexact=key,variation_value__iexact=value)
                    # print(variation)
                    # product_variation.append(variation)
                except:
                    pass    
            

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))# get the cart using the cart_id present in the session


        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )   

        cart.save()  




        # now add the product in the cart   

        is_cart_item_exist=Cartitem.objects.filter(product=product,cart=cart).exists()

        if is_cart_item_exist:
            cart_item=Cartitem.objects.filter(product=product,cart=cart)

            # if that product exist than which variation exist of that product
            # checking the variation of the quantity



            # we need three things

            #existiong variation->from database
            #current variation_->from product variation
            #item_id->database
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            # print(ex_var_list)
            if product_variation in ex_var_list:
            #   increase the cart item quantity
                index=ex_var_list.index(product_variation)
                
                item_id=id[index]
                
            

                item=Cartitem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()

            else:
                
                item=Cartitem.objects.create(product=product,quantity=1,cart=cart)
                if(len(product_variation))>0:
                    
                  item.variations.clear()
                  item.variations.add(*product_variation)
                item.save()    
            
            
    



        
        
            # cart_item.quantity=cart_item.quantity+1;
            

        else :

            cart_item=Cartitem.objects.create(
                product= product,
                quantity=1,
                cart=cart,
            )
            if(len(product_variation))>0:
              cart_item.variations.clear()
              cart_item.variations.add(*product_variation)

            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        if album_price:
            return redirect('cart_album',album_price=album_price)
        else:
            return redirect('cart');   







def add_album_to_cart(request, album_id):
   
    # Assuming you have a way to identify the current user (e.g., through authentication)
    user = request.user

    # Get the album and the user's cart
    album = get_object_or_404(Albums, id=album_id)
    cart, created = Cart.objects.get_or_create(cart_id=user.id)

    # Check if the album is already in the cart
    existing_item = Album_item.objects.filter(user=user, product=album, cart=cart).first()

    if existing_item:
        # If the album is already in the cart, you can update the quantity or take other actions.
        existing_item.quantity = 1
        existing_item.save()
    else:
        # If the album is not in the cart, create a new Album_item object and add it to the cart.
        album_item = Album_item(user=user, product=album, cart=cart, quantity=1)
        album_item.save()

    return redirect('cart') # Redirect to the cart view after adding the album




def cart(request,total=0,quantity=0,cart_items=None,album_price=None,album_name=None):
 
   
    try:
        tax=0
        grand_total=0
        total1=0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
            cart_items1=Album_item.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
            cart_items1=Album_item.objects.filter(cart=cart,is_active=True)
       
        for cart_item in cart_items:
            cart_item.item_type = 'cartitem'
        for cart_album in cart_items1:
            cart_album.item_type = 'albumitem'

        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity

        for cart_album in cart_items1:
            total1+= (cart_album.product.price*cart_album.quantity)   
        total=total+total1
        grand_total=total+total1;

        all_cart_items = list(chain(cart_items, cart_items1))
    except ObjectDoesNotExist:
        pass    
    
 


    context={
            'album':False,
            'total':total,
            'quantity':quantity,
            'cart_items':all_cart_items,
            'tax':tax,
            'grand_total':grand_total
        }
    return render(request,'cart/cart.html',context)




def remove_cart_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_type = request.POST.get('item_type')
      
        try:
            if item_type == 'cartitem':
                item = get_object_or_404(Cartitem, id=item_id, user=request.user, is_active=True)
            elif item_type == 'albumitem':
                item = get_object_or_404(Album_item, id=item_id, user=request.user, is_active=True)
            else:
                item = None

            if item:
                item.delete()
        except:
            pass

    return redirect('cart')  # Redirect back to the cart page after removal


def remove_cart(request,id):  
    product=MovieDetail.objects.get(id=id)
    item = get_object_or_404(Cartitem, product=product, user=request.user, is_active=True)  
    item.delete()
    return   # Redirect back to the cart page after removal




@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None,album_price=None):
    tax=0
    grand_total=0
    album_sum=0
    try:
     
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
            cart_items1=Album_item.objects.filter(user=request.user,is_active=True)
        

        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
            cart_items1=Album_item.objects.filter(cart=cart,is_active=True)
       


        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity
          # Concatenate the two QuerySets into a single iterable
        for album_item in cart_items1:
            album_sum+=(album_item.product.price*album_item.quantity)
            quantity+=album_item.quantity
        tax=0
        all_cart_items = list(chain(cart_items, cart_items1))
        print(all_cart_items)
        grand_total=total+tax+album_sum;    
        print(grand_total)

    except ObjectDoesNotExist:
        pass    
    
    
    if request.method == "POST":
        form=OrderForm(request.POST)
        if form.is_valid():
            data=Order()
            data.user=request.user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.zip_code=form.cleaned_data['zip_code']
            data.country=form.cleaned_data['country']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.company_name=form.cleaned_data['company_name']
            data.order_note=form.cleaned_data['order_note']
            if album_price:

                data.total=album_price
            else:
                data.total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()



            # generating order number


            yr=int(datetime.date.today().strftime("%Y"))
            dt=int(datetime.date.today().strftime("%d"))
            mt=int(datetime.date.today().strftime("%m"))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+ str(data.id)
            data.order_number=order_number
            data.save()




            order=Order.objects.get(user=request.user,is_ordered=False,order_number=order_number)
            if album_price:
                context={
                'album':True,
                'order':order,
                'cart_items':all_cart_items,
                'grand_total':grand_total,
                 'tax':0,
                 'total':grand_total,

            }
            else:


                context={
                    'album':False,
                    'order':order,
                    'cart_items':all_cart_items,
                    'grand_total':grand_total,
                    'tax':tax,
                    'total':grand_total,

                }

            return render(request,'cart/payements.html',context)

        else:
            if album_price:
                return redirect('checkout_album',album_price=album_price)
            else:
                return redirect('checkout')    
            
    else:
        form=OrderForm()
    if album_price:
         context={
        'album':True,
        'total':album_price,
        'quantity':quantity,
        'cart_items':all_cart_items,
        'tax':0,
        'grand_total':grand_total,
        'form':form
    }
    else:
        context={
            'album':False,
            'total':total,
            'quantity':quantity,
            'cart_items':all_cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'form':form
        }
    return render(request,'cart/checkout.html',context)





def payement(request):
    
    body=json.loads(request.body)
    
    order=Order.objects.get(user=request.user,order_number=body['orderID'])
 
    # store all the information in the payemnt model
    payment=Payment.objects.create(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payement_method'],
        amount_paid=order.total,
        status=body['status'],



    )
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()



# move the cart items to order product

    cart_items=Cartitem.objects.filter(user=request.user)
    cart_items1=Album_item.objects.filter(user=request.user)
    globaldata=Separator.objects.get(user=request.user)

    for item in cart_items:
        orderproduct=Order_Product()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product_id=item.product.id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.is_ordered=True
        orderproduct.save()
        


        # for adding variation in that  particular item

        cart_item=Cartitem.objects.get(id=item.id)
        # product_variation=cart_item.variations.all()
        orderproduct=Order_Product.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        orderproduct.save()


# reduce the quantity of sold products
       
        product_item=MovieDetail.objects.get(id=item.product.id)
        # product_item.stock-=item.quantity
        product_item.save()
    for item in cart_items1:
       
        albummovie=AlbumMovie.objects.get(user=request.user,album=item.product,separator=globaldata.separator)
        orderproduct=Order_Product_album()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=request.user.id
        orderproduct.product=albummovie
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.is_ordered=True
        orderproduct.save()
        


        # for adding variation in that  particular item

        cart_item1=Album_item.objects.get(id=item.id)
        # product_variation=cart_item.variations.all()
        orderproduct=Order_Product_album.objects.get(id=orderproduct.id)
        # orderproduct.variations.set(product_variation)
        orderproduct.save()


# reduce the quantity of sold products
       
        product_item=Albums.objects.get(id=item.product.id)
        # product_item.stock-=item.quantity
        product_item.save()







# clear the cart

#  after payement sucessfull the cartitem in the cart should be clear
    Cartitem.objects.filter(user=request.user).delete()
    Album_item.objects.filter(user=request.user).delete()
    if cart_items1.count()>0:
        globaldata.separator=globaldata.separator+1
        globaldata.save()

    data={
        'order_number':order.order_number,
        'transID':payment.payment_id

    }

    return JsonResponse(data)

    return render(request,'orders/payements.html')







def order_complete(request):
    
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
   
    try:
        order=Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products=Order_Product.objects.filter(order_id=order.id)
        payement=Payment.objects.get(payment_id=transID)
        

        subtotal=0
        for i in ordered_products:
            subtotal+=i.product_price*i.quantity;

        context={
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':transID,
            'payment':payement,
            'subtotal':subtotal,
          
        }
        return render(request,'cart/order_complete.html',context)


    except(Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
         
   


from django.db.models import Value, CharField


def download_pdf(request,order_number,transId):
    order=Order.objects.get(order_number=order_number,is_ordered=True)
    ordered_products=Order_Product.objects.filter(order_id=order.id)
    ordered_products_album=Order_Product_album.objects.filter(order_id=order.id)
    order_products = list(chain(ordered_products, ordered_products_album))
    payement=Payment.objects.get(payment_id=transId)        
    subtotal=0
    for i in ordered_products:
        subtotal+=i.product_price*i.quantity;

    context={
        'order':order,
        'ordered_products':order_products,
        'order_number':order.order_number,
        'transID':transId,
        'payment':payement,
        'subtotal':subtotal,
        }

    template = loader.get_template('cart/include/invoice.html')
    html_content = template.render(context)

    # Generate PDF from the HTML content
    pdf_file = pdfkit.from_string(html_content, False)

    # Create a response with the PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')

    # Set the filename for download
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_number}.pdf"'

    return response
    
def remove_album_item(request,product_id):
    pass