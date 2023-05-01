# Generated by Django 4.2 on 2023-05-01 11:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("libray", "0021_rename_user_assignbookhistory_users_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignbookhistory",
            name="date_borrowed",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="assignbookhistory",
            name="date_returned",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]