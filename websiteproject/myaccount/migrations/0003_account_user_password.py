# Generated by Django 3.2.21 on 2023-10-21 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0002_account_is_suspended'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='user_password',
            field=models.TextField(default=''),
        ),
    ]
