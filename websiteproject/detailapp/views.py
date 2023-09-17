from django.shortcuts import render,redirect
from .models import Cart,Cartitem
from indexapp.models import MovieDetail
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart   

def details(request,product_id=1):
    li=[]
    product =MovieDetail.objects.get(pk=product_id)
    user=request.user
    cart_item=Cartitem.objects.filter(user=user)
    for item in cart_item:
        li.append(item.product)
    item=product in li

  
    context={
        'val':item,
        'product':product
    }
    return render(request,'details.html',context)




def add_cart(request,product_id):
    # if the user is login 
    current_user=request.user
     
    product=MovieDetail.objects.get(id=product_id) #get the particular product
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
        return redirect('cart');   









   
def cart(request,total=0,quantity=0,cart_items=None):
    
   
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=Cartitem.objects.filter(user=request.user,is_active=True)
        

        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=Cartitem.objects.filter(cart=cart,is_active=True)
       

        for cart_item in cart_items:
            total+=(cart_item.product.price*cart_item.quantity)
            quantity+=cart_item.quantity

        tax=(2*total)/100
        grand_total=total+tax;    


    except ObjectDoesNotExist:
        pass    
    

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart/cart.html',context)



# def cart(request):
#     return render(request,'cart/cart.html')






def remove_cart_item(request,product_id,cart_item_id):
   
    product=MovieDetail.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=Cartitem.objects.get(product=product,id=cart_item_id,user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))   
            cart_item=Cartitem.objects.get(product=product,id=cart_item_id,cart=cart) 
        if cart_item.quantity>1:
           cart_item.quantity-=1;
           cart_item.save()

        else:    
            cart_item.delete()


    except:
        pass
    return redirect('cart')    


