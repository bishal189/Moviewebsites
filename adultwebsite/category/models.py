from django.db import models

from django.utils.text import slugify 
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=True)
    slug = models.SlugField(max_length=100,  null=True)
    lang = models.CharField(max_length=3, blank=True)
    def __str__(self):
        return self.category_name;


    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    
    

    # def __str__(self):
    #   return self.category_name