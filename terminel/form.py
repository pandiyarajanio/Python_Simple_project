from django import forms
from django.contrib.auth.models import User

class userupdate(forms.ModelForm):
    username = forms.CharField(required=True,max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    class Meta:
        model = User
        fields = ['username', 'email']