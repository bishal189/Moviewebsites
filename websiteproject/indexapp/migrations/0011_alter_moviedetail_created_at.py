# Generated by Django 4.2.3 on 2023-09-20 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0010_alter_moviedetail_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedetail',
            name='created_at',
            field=models.DateField(auto_created=True, null=True),
        ),
    ]
