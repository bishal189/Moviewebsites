# Generated by Django 4.2.5 on 2023-09-28 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0019_alter_moviedetail_duration_alter_moviedetail_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moviedetail',
            name='link',
        ),
    ]
