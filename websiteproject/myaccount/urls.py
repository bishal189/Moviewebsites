
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('forget/',views.forget_password,name='forget'),
    # path('reset/<str:uidb64>/<str:token>/',views.reset,name='reset'),
    
]
