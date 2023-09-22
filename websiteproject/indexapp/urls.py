from django.urls  import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search,name='search'),
    path('search/<str:tosearch>',views.search_pagination,name='search_pagination'),
    
    path('pagination/',views.pagination,name='pagination'),
    path('scenes/',views.scenes,name='scenes'),
    path('DVD/',views.dvd,name='dvd'),
    path('stars/',views.stars,name='stars'),
    path('stars/<int:id>',views.star_detail,name='star_detail')
]
