# Generated by Django 4.2.5 on 2023-09-28 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0011_alter_productform_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productform',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
