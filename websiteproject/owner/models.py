from django.db import models
from django.utils.text import slugify
# Create your models here.
class Page(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField()
    status=models.CharField(max_length=20)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now=True)


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
            super(Page,self).save(*args,**kwargs)
        else:
            super(Page,self).save(*args,**kwargs)

    