from django.db import models
from myaccount.models import Account
from indexapp.models import MovieDetail
from albums.models import Albums,AlbumMovie



# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250 ,blank=True)
    dated_added=models.DateField(auto_now_add=True)



    def __str__(self):
        return self.cart_id

class Album_item(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Albums,on_delete=models.CASCADE,null=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()

    is_active=models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price*self.quantity;

    def __str__(self):
        return str(self.product)



class Cartitem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(MovieDetail,on_delete=models.CASCADE,null=True)
    # variations=models.ManyToManyField(Variation,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()

    is_active=models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price*self.quantity;

    def __str__(self):
        return str(self.product)

class Payment (models.Model):
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100) #paypayel
    amount_paid=models.FloatField()
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id  




class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user =models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    payment =models.ForeignKey(Payment,on_delete=models.CASCADE,blank=True,null=True,related_name='orders')
    order_number=models.CharField(max_length=20)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=100)
    zip_code=models.CharField(max_length=100)
    company_name=models.CharField(max_length=100,null=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=20)
    total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip=models.CharField(max_length=20,blank=True)
    order_note=models.TextField(max_length=100,blank=True)
    is_ordered =models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    
        

    def __str__(self):
        return self.first_name




# Create your models here.

      

class Order_Product(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment =models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(MovieDetail,on_delete=models.CASCADE)
    # variations=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    counter=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order_Product_album(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment =models.ForeignKey(Payment,on_delete=models.SET_NULL,null=True,blank=True)
    user =models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(AlbumMovie,on_delete=models.CASCADE)
    # variations=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    counter=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)


    # return self.product.product_name