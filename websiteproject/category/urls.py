from django.urls import path
from . import views
urlpatterns=[
    path('',views.category,name="category"),
    path('genre/<str:genrename>/',views.category_by_genre,name="categorybygenre"),
    path('year/<int:year>/',views.category_by_year,name="categorybyyear"),
]

