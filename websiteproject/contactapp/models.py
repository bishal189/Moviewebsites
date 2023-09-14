from django.db import models

# Create your models here.
class Contact(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.CharField(max_length=40)
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=1000)
    created_at=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.first_name
