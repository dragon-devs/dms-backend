# Generated by Django 4.2.6 on 2023-10-08 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_remove_stockproduct_net_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockreceipt',
            name='total_price',
        ),
    ]