# Generated by Django 3.1.7 on 2021-02-28 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_foodname_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='resturantuser',
            name='resturant_name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
