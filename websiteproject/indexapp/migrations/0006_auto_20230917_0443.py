# Generated by Django 3.2.21 on 2023-09-17 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_category_slug'),
        ('indexapp', '0005_alter_moviedetail_coverphoto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviedetail',
            name='genere',
        ),
        migrations.AddField(
            model_name='moviedetail',
            name='genre',
            field=models.ManyToManyField(to='category.Category'),
        ),
        migrations.DeleteModel(
            name='MovieCategory',
        ),
    ]