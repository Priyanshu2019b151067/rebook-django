# Generated by Django 3.2.3 on 2021-06-07 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donate', '0002_remove_bookdonater_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='indidonar',
            name='board',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
