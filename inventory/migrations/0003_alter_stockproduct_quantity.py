# Generated by Django 4.2.6 on 2023-10-08 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_stockproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockproduct',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
