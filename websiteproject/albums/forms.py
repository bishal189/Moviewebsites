from django import forms 
from .models import Albums

class AlbumForm(forms.ModelForm):
    class Meta:
        model=Albums
        fields='__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        if self.instance.pk:
            current_movies=self.instance.movies.all()
            self.fields['movies'].queryset=current_movies