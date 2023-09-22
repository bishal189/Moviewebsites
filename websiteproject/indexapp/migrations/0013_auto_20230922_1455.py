# Generated by Django 3.2.21 on 2023-09-22 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0012_moviedetail_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='StarsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('image', models.ImageField(null=True, upload_to='stars/')),
            ],
        ),
        migrations.AddField(
            model_name='moviedetail',
            name='stars',
            field=models.ManyToManyField(blank=True, null=True, related_name='stars', to='indexapp.StarsModel'),
        ),
    ]
