# Generated by Django 4.2.5 on 2023-10-05 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_district_area_subarea_area_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='sub_area',
            new_name='district',
        ),
    ]