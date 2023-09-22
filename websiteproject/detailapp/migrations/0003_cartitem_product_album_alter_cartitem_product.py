# Generated by Django 4.2.5 on 2023-09-22 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indexapp', '0012_moviedetail_type'),
        ('albums', '0002_albums_price'),
        ('detailapp', '0002_order_payment_order_product_order_payment_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='albums.albums'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='indexapp.moviedetail'),
        ),
    ]
