from django.urls import path 
from . import views

urlpatterns = [
    path('',views.admin,name='index_admin'),
    path('additem/',views.add_item,name='additem'),
]
