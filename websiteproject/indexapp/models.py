from django.db import models
from category.models import Category
from myaccount.models import Account
# Create your models here.
from django.utils.text import slugify 



class ImagesModel(models.Model):
    image=models.ImageField(upload_to='images/')

class StarsModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='stars/',null=True)
    haircolor=models.CharField(max_length=100,blank=True,null=True)
    height=models.FloatField(null=True,blank=True)
    view_count=models.IntegerField(default=0)
    dob=models.DateField(blank=True,null=True)

    birthplace=models.CharField(max_length=200,blank=True,null=True)
    ethnicity=models.CharField(max_length=200,blank=True,null=True)
    nationality=models.CharField(max_length=200,blank=True,null=True)
    weight=models.IntegerField(blank=True,null=True)
    eyecolor=models.CharField(max_length=200,blank=True,null=True)
    bodytype=models.CharField(max_length=200,blank=True,null=True)
    tatoo=models.CharField(max_length=600,blank=True,null=True)
    piercing=models.CharField(max_length=200,blank=True,null=True)
    breast=models.CharField(max_length=100,null=True,blank=True)




class StudioModel(models.Model):
    name=models.CharField(max_length=100,blank=True)


class MovieDetail(models.Model):
    movie_name=models.CharField(max_length=100)
    year=models.IntegerField()
    stars=models.ManyToManyField(StarsModel,related_name='stars',blank=True)
    quality=models.CharField(max_length=50,default=False)
    type=models.CharField(max_length=20,blank=True)
    coverphoto=models.ImageField(upload_to='coverphoto/',null=True)
    duration=models.IntegerField(null=True,blank=True)
    short_description=models.TextField(max_length=100000)
    images=models.ManyToManyField(ImagesModel,related_name='related_images')
    trailer=models.FileField(upload_to='trailer/',blank=True,null=True)
    price=models.FloatField()
    genre=models.ManyToManyField(Category,blank=True)
    studio=models.ForeignKey(StudioModel,on_delete=models.CASCADE,blank=True,null=True)
    slug=models.SlugField(unique=True,blank=False)
    created_at=models.DateField(auto_now=True,null=True)
    view_count=models.IntegerField(default=0)
    cart_count=models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.movie_name)
        super(MovieDetail, self).save(*args, **kwargs)



    def __str__(self):
        return self.movie_name   
    

class FavouritesModel(models.Model):
    user=models.ForeignKey(Account,blank=True,null=True,on_delete=models.CASCADE)
    favourite_movies=models.ManyToManyField(MovieDetail)