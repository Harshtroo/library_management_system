from django import forms
from django.contrib.auth.models import User
from .models import User,Book
from base.constance import Role

class UserForm(forms.ModelForm):
    '''user forms'''
    # password = forms.CharField(widget=forms.PasswordInput())
    # role =
    class Meta:
        '''userform meta class'''
        model = User
        fields = ["first_name","last_name","email","username","role"]

    def save(self, commit=False):
        instance = super().save(commit=True)
        instance.set_password(instance.username + '@1234')
        if commit:
            instance.save()
        return instance

class AddBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["book_name","author_name","price","quantity"]
    
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super(AddBook, self).save(*args, **kwargs)