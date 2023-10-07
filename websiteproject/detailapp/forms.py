from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','address_line_1','zip_code','country','state','city','order_note','company_name']
        widgets = {
          'order_note': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }

    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields ['first_name'].widget.attrs['placeholder']='Enter first name'      
        self.fields ['last_name'].widget.attrs['placeholder']='Enter last name'      
        self.fields ['email'].widget.attrs['placeholder']='Enter email Address'      
        self.fields ['phone'].widget.attrs['placeholder']='Enter phone number'      
        self.fields ['address_line_1'].widget.attrs['placeholder']='Enter address_line_1'      
        self.fields ['zip_code'].widget.attrs['placeholder']='Enter Zip code'      
        self.fields ['country'].widget.attrs['placeholder']='Enter country name'      
        self.fields ['state'].widget.attrs['placeholder']='Enter state'      
        self.fields ['city'].widget.attrs['placeholder']='Enter city'      
        self.fields ['order_note'].widget.attrs['placeholder']='Enter order note'      
        self.fields ['company_name'].widget.attrs['placeholder']='Enter company name'      
        
        for field in self.fields:
            self.fields [field].widget.attrs['class']='form-control'
