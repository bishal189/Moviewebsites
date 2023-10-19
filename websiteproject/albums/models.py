from django.db import models
from indexapp.models import MovieDetail
# Create your models here.
from category.models import Category
from myaccount.models import Account


class Albums(models.Model):
    coverphoto=models.ImageField(upload_to='albums/')
    album_name=models.CharField(max_length=100)
    limit=models.IntegerField(blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    genre=models.ManyToManyField(Category,blank=True)  
    created_at=models.DateField(auto_now=True,blank=True)  
    type=models.CharField(max_length=20,blank=True)
    lang=models.CharField(max_length=3,blank=True)


    def __str__(self):
        return self.album_name



class AlbumMovie(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    album=models.ForeignKey(Albums,on_delete=models.CASCADE)
    movies=models.ManyToManyField(MovieDetail)
    counter=models.IntegerField(blank=True,null=True)
    separator=models.IntegerField(null=True)



class Separator(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    separator=models.IntegerField(default=0)

