# Generated by Django 4.2.6 on 2023-10-11 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_alter_district_province'),
        ('distribution', '0016_alter_employeesprofile_email'),
        ('inventory', '0012_remove_stockreceipt_invoice_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockreceipt',
            name='discount',
            field=models.FloatField(default=10.0),
        ),
        migrations.CreateModel(
            name='SalesInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('discount', models.FloatField(default=10.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
                ('salesman', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.employeesprofile')),
            ],
        ),
    ]