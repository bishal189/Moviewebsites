from django.urls import path

from . import views
urlpatterns=[
    path('cart/',views.cart,name="cart"),
    path('cart/<int:album_price>/<str:album_name>',views.cart,name="cart_album"),

    path('checkout/',views.checkout,name='checkout'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('checkout/<int:album_price>',views.checkout,name='checkout_album'),

    path('payement/',views.payement,name='payement'),
    path('<slug:slug>/',views.details,name="details"),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_item/<int:product_id>/',views.remove_cart_item,name='remove_item'),
    path('remove_album/<int:album_id>',views.remove_album,name='remove_album'),
    path('add_cart/<int:product_id>/<int:album_price>/',views.add_cart,name='add_cart_album'),
    path('generate_invoice/<order_number>/<transId>',views.download_pdf,name='download_pdf'),
]   
