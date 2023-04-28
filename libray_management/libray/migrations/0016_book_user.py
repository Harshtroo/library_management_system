# Generated by Django 4.2 on 2023-04-28 10:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("libray", "0015_remove_book_show_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="user",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
