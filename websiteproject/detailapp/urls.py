from django.urls import path

from . import views
urlpatterns=[
    path('<slug:slug>/',views.details,name="details"),
    path('cart/',views.cart,name="cart"),
    path('add_cart/<int:product_id>',views.add_cart,name='add_cart'),
    path('remove_item/<int:product_id>/<int:cart_item_id>',views.remove_cart_item,name='remove_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('payement/',views.payement,name='payement'),
    path('order_complete/',views.order_complete,name='order_complete')

]   
