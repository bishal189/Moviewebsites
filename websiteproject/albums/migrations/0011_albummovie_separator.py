# Generated by Django 4.2.5 on 2023-10-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0010_albums_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='albummovie',
            name='separator',
            field=models.IntegerField(null=True),
        ),
    ]
