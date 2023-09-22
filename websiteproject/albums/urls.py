from django.urls import path
from . import views
urlpatterns=[
    path('',views.album,name="album"),
    path('<int:id>/',views.album_detail,name="album_detail"),
]

