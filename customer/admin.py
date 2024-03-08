from django.contrib import admin

from .models import *


# Register your models here.

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'province']
    search_fields = ['name']


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'district']
    search_fields = ['name']


@admin.register(SubArea)
class SubAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'area']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'district', 'area', 'sub_area', 'address']
    search_fields = ['name']


