# Generated by Django 4.0.4 on 2022-06-02 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_bid_bid_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='end_auction',
            field=models.BooleanField(default=False),
        ),
    ]
