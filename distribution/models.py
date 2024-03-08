import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from backend import settings


class DistributionProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to="distribution_logo")
    description = models.TextField(blank=True)
    warranty = models.TextField(blank=True)
    signature = models.ImageField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class EmployeesProfile(models.Model):
    POSITIONS = (
        ('Manager', 'Manager / CEO / Owner'),
        ('Counter', 'Counter'),
        ('SalesMan', 'Sales Man'),
        ('Steward', 'Steward'),
    )
    distribution = models.ForeignKey(DistributionProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to="employees_picture")
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=10, choices=POSITIONS, default='SalesMan')
    salary = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class CompanyProfile(models.Model):
    distribution = models.ForeignKey(DistributionProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    picture = models.ImageField(null=True, blank=True, upload_to="companies_logo")
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class ProductForm(models.Model):
    CATEGORIES = (
        ('syp', 'Syrup'),
        ('tab', 'Tablet'),
        ('drops', 'Drops'),
        ('injection', 'Injection'),
        ('sachet', 'Sachet'),
        ('other', 'Other'),
    )

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    category = models.CharField(max_length=10, choices=CATEGORIES, default='other')
    percentage = models.FloatField(default=10.0)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Check if a product with the same company and name already exists
        existing_product = ProductForm.objects.filter(
            company=self.company,
            name=self.name
        ).exclude(pk=self.pk)  # Exclude the current instance when checking for duplicates

        if existing_product.exists():
            raise ValidationError("A product with the same company and name already exists.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
