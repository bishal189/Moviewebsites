# Generated by Django 4.2.5 on 2023-10-04 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0008_remove_albums_movies_albummovie'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albums',
            name='counter',
        ),
        migrations.AddField(
            model_name='albummovie',
            name='counter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]