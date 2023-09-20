from django.db import models
from myaccount.models import Account
from indexapp.models import MovieDetail
# Create your models here.

class Comment(models.Model):

    comment_text=models.CharField(max_length=10000)
    created_at=models.DateTimeField(auto_now_add=True)
    User=models.ForeignKey(Account,on_delete=models.CASCADE,null=False)
    Movie=models.ForeignKey(MovieDetail,on_delete=models.CASCADE,null=True)
    # like=models.IntegerField(default=0)
    # dislike=models.IntegerField(default=0)