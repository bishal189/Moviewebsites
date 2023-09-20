from django.urls import path

from . import views

urlpatterns = [
    path('add/<int:id>',views.add_comment,name='add_comment'),
]
