# Generated by Django 4.2.6 on 2023-10-13 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_alter_salesproduct_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesproduct',
            old_name='product',
            new_name='stock_product',
        ),
    ]
