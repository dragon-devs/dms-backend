# Generated by Django 4.2.6 on 2023-10-10 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_rename__discount_stockreceipt_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockreceipt',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='stockreceipt',
            name='discount',
            field=models.FloatField(default=15.0),
        ),
    ]
