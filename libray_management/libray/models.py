from django.db import models
from django.contrib.auth.models import AbstractUser
from base.constance import Role
# Create your models here.


class User(AbstractUser):    
    username = models.CharField(max_length=100,unique=True)
    role = models.CharField(max_length=10,choices=Role.choices())
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        '''soft delete funcction'''
        self.is_deleted= True
        self.save()


class Book(models.Model):
    book_image = models.ImageField(upload_to='media/images/',max_length=100)
    book_name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)
    