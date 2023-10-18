from django.urls  import path
from . import views
from django.utils.translation import gettext as _
urlpatterns = [
    path('',views.home,name='home'),
    path('search/',views.search,name='search'),
    path('pages/<str:slug>',views.pageshow,name='pageshow'),
    path('search/<str:tosearch>',views.search_pagination,name='search_pagination'),
    path('add_favourites/<int:id>',views.add_favourites,name='add_favourites'),
    path('remove_favourites/<int:id>',views.remove_favourites,name='remove_favourites'),
    path('pagination/',views.pagination,name='pagination'),
    path('scenes/',views.scenes,name='scenes'),
    path(_('DVD/'),views.dvd,name='dvd'),
    path(_('stars/'), views.stars, name='stars'),
    path('stars/<int:id>',views.star_detail,name='star_detail'),
    path('studio/<int:id>',views.studio_detail,name='studio_detail'),
    path('photosets/',views.photosets,name='photosets'),
]
