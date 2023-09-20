from indexapp.models import MovieDetail
from django import forms
class movie_form(forms.ModelForm):
    class Meta:
        model = MovieDetail
        fields='__all__'
        exclude = ('slug',)
        # fields = ['movie_name','year','duration','coverphoto','short_description','thumbnail','trailer','price','quality','link']
        widgets = {
            'duration': forms.TimeInput(format='%H:%M')
        }

#     def __init__(self,*args,**kwargs):
#         super(movie_form,self).__init__(*args,**kwargs)     
#         self.fields ['movie_name'].widget.attrs['placeholder']='enter a title'      
#         self.fields ['coverphoto'].widget.attrs['placeholder']='coverphoto'      
#         self.fields ['year'].widget.attrs['placeholder']='Enter a year'      
#         self.fields ['duration'].widget.attrs['placeholder']='runnnig time'      
#         self.fields ['short_description'].widget.attrs['placeholder']='Enter a description'      
#         self.fields ['thumbnail'].widget.attrs['placeholder']='Enter a thumbnail'      
#         self.fields ['trailer'].widget.attrs['placeholder']='Enter a trailer'      
#         self.fields ['price'].widget.attrs['placeholder']='Enter a price'      
             
     
#         for field in self.fields:
#             pass
#             # self.fields [field].widget.attrs['class']='sign__input' 
        


class MovieDetailForm(forms.ModelForm):
    class Meta:
        model = MovieDetail
        fields = ['movie_name', 'year', 'quality', 'coverphoto', 'duration', 'short_description', 'trailer', 'price', 'link']


    def __init__(self,*args,**kwargs):
        super(MovieDetailForm,self).__init__(*args,**kwargs)     
        self.fields ['trailer'].widget.attrs['class']='form__video-upload'      
        self.fields ['trailer'].widget.attrs['id']='form__video-upload'      
        self.fields ['trailer'].widget.attrs['type']='file'      
        self.fields ['coverphoto'].widget.attrs['id']='form__img-upload'      
        self.fields ['movie_name'].widget.attrs['class']='form__input'      
        self.fields ['short_description'].widget.attrs['class']='form__textarea'      
        self.fields ['price'].widget.attrs['class']='form__input'      
        self.fields ['year'].widget.attrs['class']='form__input'      
        self.fields ['duration'].widget.attrs['class']='form__input'      
        self.fields ['link'].widget.attrs['class']='form__input'      
        self.fields ['link'].widget.attrs['type']='link'      
        # self.fields ['images'].widget.attrs['type']='file'      
        # self.fields ['images'].widget.attrs['id']='form__gallery-upload'      
        # self.fields ['images'].widget.attrs['class']='form__gallery-upload'   
        # self.fields ['images'].widget.attrs['accept']=".png, .jpg, .jpeg" 

        # self.fields ['price'].widget.attrs['placeholder']='Enter a price'      
             
     
#         for field in self.fields:
#             pass
#             # self.fields [field].widget.attrs['class']='sign__input' 
