from django import forms
from .models import User, Product, Banner
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'picture', 'email', 'telephone')
        widgets = {
            'picture': forms.FileInput(attrs={'class':'custom-file-input','onchange':'readURL(this);'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', }),
            'last_name': forms.TextInput(attrs={'class':'form-control', }),
            'email': forms.TextInput(attrs={'class':'form-control', 'required': True, 'type':'email'}),
            'telephone': forms.TextInput(attrs={'class':'form-control', }),
            'username': forms.TextInput(attrs={'class':'form-control', }),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'reference', 'description', 'picture1', 'picture2', 'picture3', 'picture4', 'category', 'pdf', 'language', 'price', 'flag', 'min_order', 'flagbackcolor', 'indexed')

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ('name', 'picture', 'language')

