from django.urls import path
from . import views
urlpatterns=[
    path('',views.category,name="category"),
    path('filter/',views.category_filter,name="category_filter"),
    path('genre/<str:genrename>/',views.category_by_genre,name="categorybygenre"),
   
]
