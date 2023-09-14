from django.db import models

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=50)
    slug=models.SlugField(unique=True,blank=False)
