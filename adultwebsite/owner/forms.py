from indexapp.models import MovieDetail,StarsModel
from django import forms
from albums.models import Albums
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
        fields = ['movie_name', 'year', 'quality', 'coverphoto', 'duration', 'short_description', 'trailer', 'price','images','videoname']
        images = forms.ImageField(required=False)


    def __init__(self,*args,**kwargs):
        super(MovieDetailForm,self).__init__(*args,**kwargs)     
        self.fields ['trailer'].widget.attrs['class']='form__video-upload'      
        self.fields ['trailer'].widget.attrs['id']='form__video-upload'      
        self.fields ['trailer'].widget.attrs['type']='file'      
        self.fields ['trailer'].widget.attrs['placeholder']='trailer'      
        self.fields ['coverphoto'].widget.attrs['id']='form__img-upload'      
        self.fields ['coverphoto'].widget.attrs['placeholder']='coverphoto'      
        self.fields ['movie_name'].widget.attrs['class']='form__input'      
        self.fields ['movie_name'].widget.attrs['placeholder']='movie name'      
        self.fields ['short_description'].widget.attrs['class']='form__textarea'      
        self.fields ['short_description'].widget.attrs['placeholder']='descriptions'      
        self.fields ['price'].widget.attrs['class']='form__input'      
        self.fields ['price'].widget.attrs['placeholder']='price'      
        self.fields ['videoname'].widget.attrs['class']='form__input'      
        self.fields ['videoname'].widget.attrs['placeholder']='videoname'      
        # self.fields ['price'].widget.attrs['class']='form__input'      
        self.fields ['year'].widget.attrs['class']='form__input'      
        self.fields ['year'].widget.attrs['placeholder']='year'      
        self.fields ['duration'].widget.attrs['class']='form__input'      
        self.fields ['duration'].widget.attrs['placeholder']='duration'      
        self.fields ['images'].widget.attrs['class']='form__gallery-upload'      
        self.fields ['images'].widget.attrs['id']='form__gallery-upload'      
        self.fields ['images'].widget.attrs['type']='file'      
        self.fields ['images'].widget.attrs['accept']='.png, .jpg, .jpeg'      
        self.fields ['images'].widget.attrs['data_name']='#gallery1'  
        self.fields ['images'].widget.attrs['placeholder']='images'  
          



class Album_form(forms.ModelForm):
    class Meta:
        model = Albums
        fields = ['coverphoto', 'album_name', 'limit',  'price', 'genre']

    def __init__(self,*args,**kwargs):
        super(Album_form,self).__init__(*args,**kwargs)     
        # self.fields ['trailer'].widget.attrs['class']='form__video-upload'      
        # self.fields ['trailer'].widget.attrs['id']='form__video-upload'      
        # self.fields ['trailer'].widget.attrs['type']='file'      
        self.fields ['coverphoto'].widget.attrs['id']='form__img-upload'      
        self.fields ['album_name'].widget.attrs['class']='form__input'      
        self.fields ['limit'].widget.attrs['class']='form__input'      
        self.fields ['price'].widget.attrs['class']='form__input'      
        self.fields ['genre'].widget.attrs['class']='form__input'      
        # self.fields ['short_description'].widget.attrs['class']='form__textarea'      
        # self.fields ['price'].widget.attrs['class']='form__input'      
        # self.fields ['year'].widget.attrs['class']='form__input'      
        # self.fields ['duration'].widget.attrs['class']='form__input'  

    




# for the stars 

# class Stars_form(forms.ModelForm):
#     class Meta:
#         model = StarsModel
#         fields = "__all__"
#     def __init__(self,*args,**kwargs):
#         super(Stars_form,self).__init__(*args,**kwargs)   
#         self.fields ['name'].widget.attrs['class']='form__input'
#         self.fields ['name'].widget.attrs['placeholder']='Enter Name'
#         self.fields ['image'].widget.attrs['id']='form__img-upload'  
#         self.fields ['haircolor'].widget.attrs['class']='form__input'   
#         self.fields ['haircolor'].widget.attrs['placeholder']='haircolor'   
#         self.fields ['height'].widget.attrs['class']='form__input'   
#         self.fields ['height'].widget.attrs['placeholder']='height'   
#         self.fields ['view_count'].widget.attrs['class']='form__input'   
#         self.fields ['view_count'].widget.attrs['placeholder']='view_count'   
#         self.fields ['dob'].widget.attrs['class']='form__input'   
#         self.fields ['dob'].widget.attrs['placeholder']='DOB'   
#         self.fields ['birthplace'].widget.attrs['class']='form__input'   
#         self.fields ['birthplace'].widget.attrs['placeholder']='birthplace'   
#         self.fields ['ethnicity'].widget.attrs['class']='form__input'   
#         self.fields ['ethnicity'].widget.attrs['placeholder']='ethnicity'   
#         self.fields ['nationality'].widget.attrs['class']='form__input'   
#         self.fields ['nationality'].widget.attrs['placeholder']='nationality'      
#         self.fields ['weight'].widget.attrs['class']='form__input'   
#         self.fields ['weight'].widget.attrs['placeholder']='weight'   
#         self.fields ['tatoo'].widget.attrs['class']='form__input'      
#         self.fields ['tatoo'].widget.attrs['placeholder']='Tatoo'      
#         self.fields ['piercing'].widget.attrs['class']='form__input' 
#         self.fields ['piercing'].widget.attrs['placeholder']='piercing' 
#         self.fields ['breastsize'].widget.attrs['class']='form__input' 
#         self.fields ['breastsize'].widget.attrs['placeholder']='breastsize' 
#         self.fields ['bodymarking'].widget.attrs['class']='form__input' 
#         self.fields ['bodymarking'].widget.attrs['placeholder']='bodymarking' 
#         self.fields ['currentstatus'].widget.attrs['class']='form__input' 
#         self.fields ['currentstatus'].widget.attrs['placeholder']='currentstatus' 
#         self.fields ['gender'].widget.attrs['class']='form__input' 
#         self.fields ['gender'].widget.attrs['placeholder']='Gender' 
#         self.fields ['modeltype'].widget.attrs['class']='form__input' 
#         self.fields ['modeltype'].widget.attrs['placeholder']='Model Type'
#         self.fields ['eyecolor'].widget.attrs['class']='form__input' 
#         self.fields ['eyecolor'].widget.attrs['placeholder']='Eyecolor' 
#         self.fields ['bodytype'].widget.attrs['class']='form__input' 
#         self.fields ['bodytype'].widget.attrs['placeholder']='Body Type' 
         
        # self.fields ['images'].widget.attrs['class']='form__gallery-upload'      
        # self.fields ['images'].widget.attrs['id']='form__gallery-uploa'      
        # self.fields ['images'].widget.attrs['type']='file'      
        # self.fields ['images'].widget.attrs['accept']='.png, .jpg, .jpeg'      
        # self.fields ['images'].widget.attrs['data_name']='#gallery1'     