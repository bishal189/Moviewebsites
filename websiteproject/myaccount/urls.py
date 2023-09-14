
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.Register,name='signup'),
    path('login/',views.Login,name='login'),
    
]
