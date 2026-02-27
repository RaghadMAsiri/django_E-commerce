from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'  
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ادخل بريدك الالكتروني'
        })
    )
    
    subject = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ادخل عنوان الرسالة '
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'ادخل الرسالة  '
        })
    )
    
class RegisterForm (UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ادخل بريدك الالكتروني'
        })
    )
    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        widget={
            'username':forms.TextInput(attrs={'class':'form-control text-center'}),
            'password1':forms.PasswordInput(attrs={'class':'form-control text-center'}),
            'password2':forms.PasswordInput(attrs={'class':'form-control text-center'})
        }
        
