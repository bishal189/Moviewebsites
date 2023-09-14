from django.db import models
from myaccount.models import Account

# Create your models here.

class Comment(models.Model):
    username=models.CharField(max_length=25)
    comment_text=models.CharField(max_length=10000)
    created_at=models.DateTimeField(auto_now_add=True)
    User=models.ForeignKey(Account,on_delete=models.CASCADE)