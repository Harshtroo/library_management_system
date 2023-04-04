from django import forms
from django.contrib.auth.models import User
from .models import User
from base.constance import Role

class UserForm(forms.ModelForm):
    '''user forms'''
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        '''userform meta class'''

        model = User
        fields = ["username","fullname","role"]

    def save(self, commit=False):
        instance = super().save(commit=True)
        instance.set_password(instance.username +'@1234')
        if commit:
            instance.save()
        return instance