from django.db import models
from category.models import Category
# Create your models here.

class MovieDetail(models.Model):
    movie_name=models.CharField(max_length=100)
    year=models.IntegerField()
    duration=models.TimeField()
    short_description=models.CharField(max_length=100000)
    thumbnail=models.ImageField(upload_to='thumbanils')
    trailer=models.FileField(upload_to='trailer')
    price=models.IntegerField()
    slug=models.SlugField(unique=True,blank=False)


class MovieCategory(models.Model):
    movie_foreign=models.ForeignKey(MovieDetail,on_delete=models.CASCADE,null=False)
    category_foreign=models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
