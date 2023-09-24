# Generated by Django 4.2.3 on 2023-09-24 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0016_alter_moviedetail_stars'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudioModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='moviedetail',
            name='studio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='indexapp.studiomodel'),
        ),
    ]
