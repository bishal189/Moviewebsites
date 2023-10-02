from django.db import models
from indexapp.models import MovieDetail
# Create your models here.
from category.models import Category

class Albums(models.Model):
    coverphoto=models.ImageField(upload_to='albums/')
    album_name=models.CharField(max_length=100)
    movies=models.ManyToManyField(MovieDetail,related_name='albums',blank=True)
    limit=models.IntegerField(blank=True,null=True)
    counter=models.IntegerField(blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    genre=models.ManyToManyField(Category)  
    created_at=models.DateField(auto_now=True,blank=True)  


    def __str__(self):
        return self.album_name