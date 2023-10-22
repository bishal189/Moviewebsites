from django.urls import path
from . import views
urlpatterns = [
    path('',views.download_list,name='download_list'),
    path('getftp/',views.get_ftp,name='getftp'),

    path('<str:filename>/', views.file_download, name='file_download'),
    path('packages/<int:id>',views.package_list,name='package_list'),
    path('inrease/<int:id>',views.inc_counter,name='inc_counter'),

]
