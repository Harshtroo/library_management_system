from django.db import models
from django.contrib.auth.models import AbstractUser
from base.constance import Role
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    role = models.CharField(max_length=10, choices=Role.choices())
    is_deleted = models.BooleanField(default=False)

    def soft_delete(self):
        """soft delete funcction"""
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.username

class Book(models.Model):
    book_image = models.ImageField(upload_to="books/", max_length=100)
    book_name = models.CharField(max_length=200,unique=True)
    author_name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_name

class AssignedBook(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=False)
    book = models.ForeignKey(Book,on_delete= models.CASCADE)
    date_borrowed = models.DateTimeField(default=timezone.now)
    date_returned = models.DateTimeField(null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    
    def soft_delete(self):
        '''soft delete funcction'''
        self.is_deleted= True
        self.save()

    def __str__(self) -> str:
        return self.book.book_name