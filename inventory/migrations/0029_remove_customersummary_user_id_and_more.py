# Generated by Django 4.2.6 on 2023-10-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_alter_customersummary_invoices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customersummary',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='customersummary',
            name='invoices',
            field=models.ManyToManyField(limit_choices_to={'customer__id': models.F('customer')}, to='inventory.salesinvoice'),
        ),
    ]
