# Generated by Django 4.2 on 2023-05-01 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("libray", "0019_alter_assignbookhistory_book_alter_book_book_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignbookhistory",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="libray.book"
            ),
        ),
    ]