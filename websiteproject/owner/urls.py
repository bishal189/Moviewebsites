
# from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard' ),
    path('add_item/',views.add_item,name='add_item'),
    path('catalog/',views.catalog,name='catalog'),
    path('users/',views.user_list,name='user_list'),
    path('add_stars/',views.add_stars,name='add_stars'),
    path('add_studio/',views.add_studio,name='add_studio'),
    path('add_genre/',views.add_genre,name='add_genre'),

    path('edit_user/',views.edit_user,name='edit_user'),
    path('show_transactions/',views.show_transactions,name='transactions'),
    path('show_transactions/country',views.show_transactions_country,name='transactions_country'),
    path('show_transactions/product',views.show_transactions_product,name='transactions_product'),
    

    path('add_packages/',views.add_album,name='add_album'),
    path('suspend_user/<int:id>/',views.suspended_user,name='suspend_user'),
    path('active_user/<int:id>/',views.active_user,name='active_user'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('delete_user/<int:id>/',views.user_delete_user,name='user_delete_user'),

    path('edit_movie/<int:id>',views.edit_movie,name='edit_movie'),
    path('edit_album/<int:id>',views.edit_album,name='edit_album'),
    path('remove_movie/<int:id>',views.remove_movie,name='remove_movie'),
    path('remove_album/<int:id>',views.remove_album,name='remove_album'),

  
]
