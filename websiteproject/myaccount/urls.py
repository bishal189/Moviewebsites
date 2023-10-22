
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forget/',views.forget_password,name='forget'),
    path('reset_password/',views.reset_password,name='confrim_password'),
    path('profile/',views.profile,name='profile'),
    path('changed_password/',views.changed_password,name='changed_password'),
    path('activate/<uidb64>/<token>/', views.activate,name='activate'),
    path('password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset'),
   
    
]
