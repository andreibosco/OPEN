from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput, TextInput
from OPEN.userprofile.models import UserProfile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        widgets = {
            'password': PasswordInput(),
            'username': TextInput(attrs={'placeholder': 'Username'}),
            'password': TextInput(attrs={'placeholder': 'Password'}),
            'email': TextInput(attrs={'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'placeholder': 'Last Name'}),    
        }

        
class UserProfileForm( ModelForm ):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'address', 'country', 'city', 'phone', 'date_of_birth', 'website']
        widgets = {
            'address': TextInput(attrs={'placeholder': 'Address'}),
            'city': TextInput(attrs={'placeholder': 'City'}),
            'phone': TextInput(attrs={'placeholder': 'Phone'}),
            'date_of_birth': TextInput(attrs={'placeholder': 'Date of Birth'}),            
            'website': TextInput(attrs={'placeholder': 'Web Site'}),
        }
