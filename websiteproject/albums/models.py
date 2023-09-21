from django.db import models
from indexapp.models import MovieDetail
# Create your models here.

class Albums(models.Model):
    album_name=models.CharField(max_length=100)
    description=models.TextField(max_length=10000)
    movies=models.ManyToManyField(MovieDetail,related_name='albums',blank=True)


    def __str__(self):
        return self.album_name