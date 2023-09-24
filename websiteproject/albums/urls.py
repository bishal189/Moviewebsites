from django.urls import path
from . import views
urlpatterns=[
    path('',views.album,name="album"),
    path('<int:id>/',views.album_detail,name="album_detail"),
    path('inc_movie/<int:album_id>/<int:movie_id>/',views.inc_counter,name="inc_counter"),
    path('dec_movie/<int:album_id>/<int:movie_id>/',views.dec_counter,name="dec_counter"),

]

