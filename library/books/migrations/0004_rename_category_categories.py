# Generated by Django 5.0.2 on 2024-02-28 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_category_book_quantity_book_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Categories',
        ),
    ]
