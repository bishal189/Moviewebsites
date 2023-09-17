from django.db import models
from myaccount.models import Account
from indexapp.models import MovieDetail



# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250 ,blank=True)
    dated_added=models.DateField(auto_now_add=True)



    def __str__(self):
        return self.cart_id


class Cartitem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(MovieDetail,on_delete=models.CASCADE)
    # variations=models.ManyToManyField(Variation,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()

    is_active=models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price*self.quantity;

    def __str__(self):
        return str(self.product)






