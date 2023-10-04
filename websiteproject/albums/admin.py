from django.contrib import admin
from .forms import AlbumForm
from .models import *
# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    form=AlbumForm
admin.site.register(Albums,AlbumAdmin)
admin.site.register(AlbumMovie)