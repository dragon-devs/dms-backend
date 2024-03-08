# Generated by Django 4.2.5 on 2023-09-27 16:47

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('distribution', '0009_alter_companyprofile_email_alter_companyprofile_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='ProductForm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='products_images')),
                ('expire_date', models.DateField()),
                ('price', models.IntegerField()),
                ('category', models.CharField(choices=[('syringe', 'Syringe'), ('tab', 'Tablets'), ('pill', 'Pill'), ('powder', 'Powder'), ('first_aid', 'First Aid Kit'), ('drop', 'Drops'), ('capsules', 'Capsules')], default='tab', max_length=10)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='distribution.companyprofile')),
            ],
        ),
    ]