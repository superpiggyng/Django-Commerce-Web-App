# Generated by Django 5.0 on 2024-04-20 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_auctionlisting_id_alter_bid_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='brand',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
