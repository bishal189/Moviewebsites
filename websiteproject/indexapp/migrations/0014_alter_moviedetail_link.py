# Generated by Django 3.2.21 on 2023-09-22 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0013_auto_20230922_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedetail',
            name='link',
            field=models.URLField(blank=True, default=False),
        ),
    ]
