# Generated by Django 3.2.21 on 2023-10-20 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0003_alter_page_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='lang',
            field=models.CharField(blank=True, max_length=2),
        ),
    ]
