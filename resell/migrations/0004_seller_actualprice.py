# Generated by Django 3.2.3 on 2021-06-01 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resell', '0003_seller_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='actualprice',
            field=models.IntegerField(default=0),
        ),
    ]