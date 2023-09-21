from django.db import models
from indexapp.models import MovieDetail
# Create your models here.

class Albums(models.Model):
    coverphoto=models.ImageField(upload_to='albums/')
    album_name=models.CharField(max_length=100)
    description=models.TextField(max_length=10000)
    movies=models.ManyToManyField(MovieDetail,related_name='albums',blank=True)
    price=models.IntegerField(blank=True,null=True)


    def __str__(self):
        return self.album_name