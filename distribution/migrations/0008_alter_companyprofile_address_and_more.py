# Generated by Django 4.2.5 on 2023-09-27 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0007_companyprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='companyprofile',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
