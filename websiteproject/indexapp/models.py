from django.db import models
from category.models import Category
# Create your models here.
from django.utils.text import slugify 

class MovieDetail(models.Model):
    movie_name=models.CharField(max_length=100)
    year=models.IntegerField()
    quality=models.CharField(max_length=50,default=False)
    coverphoto=models.ImageField(upload_to='coverphoto/',null=True)
    duration=models.IntegerField(null=True)
    short_description=models.TextField(max_length=100000)
    thumbnail=models.ImageField(upload_to='thumbanils/')
    trailer=models.FileField(upload_to='trailer/')
    price=models.IntegerField()
    genere=models.CharField(max_length=100,null=True,default=False)
    slug=models.SlugField(unique=True,blank=False)
    link=models.URLField(unique=False,blank=False, default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.movie_name)
        super(MovieDetail, self).save(*args, **kwargs)



    def __str__(self):
        return self.movie_name    


class MovieCategory(models.Model):
    movie_foreign=models.ForeignKey(MovieDetail,on_delete=models.CASCADE,null=False)
    category_foreign=models.ForeignKey(Category,on_delete=models.CASCADE,null=False)
