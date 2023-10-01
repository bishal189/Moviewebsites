from .models import Cart,Cartitem,Album_item
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart    


def counter(request):
    cart_count=0
    cart_count1=0
    if 'admin' in request.path:
        return {}

    else:
        try:
            cart=Cart.objects.filter(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_items=Cartitem.objects.all().filter(user=request.user)
                cart_items1=Album_item.objects.all().filter(user=request.user)


            else:    
               cart_items=Cartitem.objects.all().filter(cart=cart[:1])
               cart_items1=Album_item.objects.all().filter(cart=cart[:1])
            for item in cart_items:
                cart_count=cart_count+item.quantity
            
            for item1 in cart_items1:
                cart_count1=cart_count1+item1.quantity
            
            cart_count2=cart_count+cart_count1
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count2)        