# Generated by Django 4.2.5 on 2023-10-03 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0015_alter_companyprofile_id_alter_employeesprofile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeesprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]