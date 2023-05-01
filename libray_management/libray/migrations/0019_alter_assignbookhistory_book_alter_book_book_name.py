# Generated by Django 4.2 on 2023-05-01 07:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("libray", "0018_remove_book_user_remove_assignbookhistory_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignbookhistory",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="libray.book",
                to_field="book_name",
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="book_name",
            field=models.CharField(max_length=200, unique=True),
        ),
    ]