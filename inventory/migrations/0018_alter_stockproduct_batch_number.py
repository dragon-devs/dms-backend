# Generated by Django 4.2.6 on 2023-10-12 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_salesproduct_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockproduct',
            name='batch_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
