# Generated by Django 4.2.5 on 2023-09-20 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0009_moviedetail_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedetail',
            name='created_at',
            field=models.DateField(auto_created=True, default='24 Oct 2021', null=True),
        ),
    ]