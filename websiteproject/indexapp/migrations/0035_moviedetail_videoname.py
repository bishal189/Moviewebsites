# Generated by Django 3.2.21 on 2023-10-20 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0034_remove_starsmodel_lang'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviedetail',
            name='videoname',
            field=models.TextField(blank=True),
        ),
    ]
