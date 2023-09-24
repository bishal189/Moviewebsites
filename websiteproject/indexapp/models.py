from django.db import models
from category.models import Category
# Create your models here.
from django.utils.text import slugify 
class ImagesModel(models.Model):
    image=models.ImageField(upload_to='images/')

class StarsModel(models.Model):
    name=models.CharField(max_length=100,null=True)
    image=models.ImageField(upload_to='stars/',null=True)
    haircolor=models.CharField(max_length=100,blank=True,null=True)
    height=models.FloatField(null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)


class StudioModel(models.Model):
    name=models.CharField(max_length=100,blank=True)


class MovieDetail(models.Model):
    movie_name=models.CharField(max_length=100)
    year=models.IntegerField()
    stars=models.ManyToManyField(StarsModel,related_name='stars',blank=True)
    quality=models.CharField(max_length=50,default=False)
    type=models.CharField(max_length=20,blank=True)
    coverphoto=models.ImageField(upload_to='coverphoto/',null=True)
    duration=models.IntegerField(null=True)
    short_description=models.TextField(max_length=100000)
    images=models.ManyToManyField(ImagesModel,related_name='related_images')
    trailer=models.FileField(upload_to='trailer/',blank=True,null=True)
    price=models.IntegerField()
    genre=models.ManyToManyField(Category)
    studio=models.ForeignKey(StudioModel,on_delete=models.SET_NULL,blank=True,null=True)
    slug=models.SlugField(unique=True,blank=False)
    link=models.URLField(unique=False,blank=True, default=False)
    created_at=models.DateField(auto_now=True,null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.movie_name)
        super(MovieDetail, self).save(*args, **kwargs)



    def __str__(self):
        return self.movie_name   


'''


class MovieCategory(models.Model):
    movie_foreign=models.ForeignKey(MovieDetail,on_delete=models.CASCADE,null=False)
    category_foreign=models.ForeignKey(Category,on_delete=models.CASCADE,null=False)

'''
