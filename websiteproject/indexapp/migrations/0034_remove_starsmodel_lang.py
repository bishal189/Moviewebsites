# Generated by Django 3.2.21 on 2023-10-19 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0033_alter_moviedetail_lang'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='starsmodel',
            name='lang',
        ),
    ]