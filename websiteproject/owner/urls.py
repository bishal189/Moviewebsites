
# from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard' ),
    path('add_item/',views.add_item,name='add_item'),
    path('catalog/',views.catalog,name='catalog'),
    path('comments/',views.comments_list,name='comments_list'),
    path('users/',views.user_list,name='user_list'),
    path('edit_user/',views.edit_user,name='edit_user'),
]
