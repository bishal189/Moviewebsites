from django.contrib import admin

# Register your models here.
from .models import *
from .forms import MovieDetailForm
class MovieDetailAdmin(admin.ModelAdmin):
    form=MovieDetailForm
admin.site.register(ImagesModel)
admin.site.register(MovieDetail,MovieDetailAdmin)
admin.site.register(StarsModel)
admin.site.register(StudioModel)
