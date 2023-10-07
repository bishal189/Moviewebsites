from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(ImagesModel)
admin.site.register(MovieDetail)
admin.site.register(StarsModel)
admin.site.register(StudioModel)
admin.site.register(FavouritesModel)
