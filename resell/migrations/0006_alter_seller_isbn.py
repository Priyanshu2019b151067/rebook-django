# Generated by Django 3.2.3 on 2021-06-25 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resell', '0005_seller_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='isbn',
            field=models.CharField(blank=True, default='xxxxxxxxxxxxx', max_length=100),
        ),
    ]
