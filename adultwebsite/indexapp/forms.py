from django import forms 
from .models import MovieDetail

class MovieDetailForm(forms.ModelForm):
    class Meta:
        model=MovieDetail
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        if self.instance.pk:
            current_genres=self.instance.genre.all()
            current_images=self.instance.images.all()
            current_stars=self.instance.stars.all()
            self.fields['stars'].queryset=current_stars
            self.fields['images'].queryset=current_images
            self.fields['genre'].queryset=current_genres
