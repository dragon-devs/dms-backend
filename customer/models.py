from django.core.exceptions import ValidationError
from django.db import models


class Province(models.Model):
   COUNTRIES = (
      ('pk', 'Pakistan'),

   )
   name = models.CharField(max_length=255)
   country = models.CharField(max_length=10, choices=COUNTRIES, default='pk')

   def __str__(self):
      return self.name


class District(models.Model):
   name = models.CharField(max_length=255)
   province = models.ForeignKey(Province, on_delete=models.CASCADE)

   def __str__(self):
      return self.name


class Area(models.Model):
   name = models.CharField(max_length=255)
   district = models.ForeignKey(District, on_delete=models.CASCADE)

   def __str__(self):
      return self.name

   def clean(self):
      # Check if an Area with the same name and district already exists
      existing_areas = Area.objects.filter(name=self.name.lower(), district=self.district)
      if self.pk:  # Exclude the current instance if it's being updated
         existing_areas = existing_areas.exclude(pk=self.pk)
      if existing_areas.exists():
         raise ValidationError('An Area with the same name already exists in this district.')

   def save(self, *args, **kwargs):
      self.clean()  # Run the custom validation
      super().save(*args, **kwargs)


class SubArea(models.Model):
   name = models.CharField(max_length=255)
   area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True)

   def __str__(self):
      return self.name


class Customer(models.Model):
   name = models.CharField(max_length=150)
   phone = models.CharField(max_length=13)
   district = models.ForeignKey(District, on_delete=models.CASCADE)
   area = models.ForeignKey(Area, on_delete=models.CASCADE)
   sub_area = models.ForeignKey(SubArea, on_delete=models.CASCADE, null=True, blank=True)

   @property
   def address(self):
      # Build the address based on related objects
      address_parts = [self.sub_area.name if self.sub_area else "",
                       self.area.name,
                       self.district.name,
                       self.district.province.name,
                       ]
      return ", ".join(filter(None, address_parts))

   def __str__(self):
      return self.name
