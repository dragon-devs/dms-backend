# Generated by Django 4.2.5 on 2023-10-05 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='district',
            name='area',
        ),
        migrations.AddField(
            model_name='subarea',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.area'),
        ),
        migrations.AlterField(
            model_name='area',
            name='sub_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.district'),
        ),
    ]