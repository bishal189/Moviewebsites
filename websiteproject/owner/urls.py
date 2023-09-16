
# from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard' ),
    path('add_item/',views.add_item,name='add_item'),
]
