from rest_framework import serializers

from .models import DistributionProfile, EmployeesProfile, CompanyProfile, ProductForm


class DistributionProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = DistributionProfile
        fields = ['id', 'user_id', 'name', 'picture', 'warranty', 'signature', 'description', 'phone', 'address',
                  'website']


class EmployeesProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeesProfile
        fields = ['id', 'name', 'picture', 'email', 'phone', 'position', 'salary']


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['id', 'name', 'picture', 'description', 'phone', 'email', 'address', 'website']


class ProductFormSerializer(serializers.ModelSerializer):
    company = serializers.CharField(read_only=True)

    class Meta:
        model = ProductForm
        fields = ['id', 'name', 'company', 'category', 'percentage', 'price']
