# Generated by Django 4.2 on 2023-04-14 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libray', '0005_book_book_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_image',
        ),
    ]
