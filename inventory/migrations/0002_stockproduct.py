# Generated by Django 4.2.6 on 2023-10-08 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0016_alter_employeesprofile_email'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(max_length=10)),
                ('batch_number', models.CharField(max_length=10)),
                ('expire_date', models.DateField()),
                ('net_price', models.FloatField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.productform')),
                ('stock_receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.stockreceipt')),
            ],
        ),
    ]
