from django.contrib import admin

from distribution.models import DistributionProfile, EmployeesProfile, CompanyProfile, ProductForm


# Register your models here.

@admin.register(DistributionProfile)
class DistributionProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user_id', 'name', 'picture', 'phone', 'address', 'website']
    search_fields = ['name']


@admin.register(EmployeesProfile)
class EmployeesProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'distribution', 'name', 'picture', 'phone', 'email', 'position', 'salary']
    search_fields = ['name', 'distribution']


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'distribution', 'name', 'picture', 'phone', 'email', 'address', 'website']
    search_fields = ['name']


@admin.register(ProductForm)
class ProductFormAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'name', 'category', 'price']
    search_fields = ['name', 'company']

