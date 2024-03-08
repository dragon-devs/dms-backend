# Generated by Django 4.2.5 on 2023-09-23 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0003_alter_employeesprofile_distribution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='employeesprofile',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='employeesprofile',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
