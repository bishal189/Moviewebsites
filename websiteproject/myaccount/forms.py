from django import forms
from .models import Account
from captcha.fields import ReCaptchaField 
from captcha.widgets import ReCaptchaV2Checkbox



class ResitrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))
    confrim_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confrim password'
    }))
    class Meta:
        model=Account
        fields=['username','email','password',]
        # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox) 

    def __init__(self,*args,**kwargs):
        super(ResitrationForm,self).__init__(*args,**kwargs)
        # self.fields ['first_name'].widget.attrs['placeholder']='Enter first name'      
        # self.fields ['last_name'].widget.attrs['placeholder']='Enter last name'      
        self.fields ['email'].widget.attrs['placeholder']='Enter email Address'      
        self.fields ['username'].widget.attrs['placeholder']='Enter username'      
             
     
        for field in self.fields:
            self.fields [field].widget.attrs['class']='sign__input'





    def clean(self):
        cleaned_data=super(ResitrationForm,self).clean()
        password=cleaned_data.get('password')
        confrim_password=cleaned_data.get('confrim_password')


        if password!=confrim_password:
            raise forms.ValidationError(
                'password does not match!.'
            )              