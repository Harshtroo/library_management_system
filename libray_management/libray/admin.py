from django.contrib import admin

# Register your models here.
from .models import User,Book,AssignedBook
admin.site.register(User)
admin.site.register(Book)
admin.site.register(AssignedBook)

