# Generated by Django 4.0.4 on 2022-05-22 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_bid_bid_author_bid_bid_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.lot'),
        ),
    ]
