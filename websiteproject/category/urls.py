from django.urls import path
from . import views
urlpatterns=[
    path('category',views.category,name="category"),
    path('',views.category_filter,name="category_filter"),
    path('<str:type>',views.category_filter,name='category_filter_type'),
    path('genre/<str:genrename>/',views.category_by_genre,name="categorybygenre"),
   
]
