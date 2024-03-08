from rest_framework import serializers
from .models import Inventory, StockReceipt, StockProduct, SalesInvoice, SalesProduct, CustomerSummary
from distribution.serializers import DistributionProfileSerializer, ProductFormSerializer
from distribution.models import CompanyProfile, ProductForm, DistributionProfile, EmployeesProfile


class InventorySerializer(serializers.ModelSerializer):
    distribution = DistributionProfileSerializer()

    class Meta:
        model = Inventory
        fields = [
            'id',
            'distribution',
            'timestamp'
        ]


class CompanyForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return CompanyProfile.objects.filter(distribution__user=self.context['request'].user)


class StockReceiptSerializer(serializers.ModelSerializer):
    company = CompanyForeignKey()

    class Meta:
        model = StockReceipt
        fields = [
            'invoice_number',
            'company',
            'discount',
            'total_price',
            'discounted_price'
        ]


class ProductForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        if request:
            stock_receipt_id = request.parser_context['kwargs']['stock_receipt_pk']
            stock_receipt = StockReceipt.objects.filter(pk=stock_receipt_id).first()
            if stock_receipt:
                selected_company = stock_receipt.company
                return ProductForm.objects.filter(company=selected_company)
        return ProductForm.objects.none()


class StockProductSerializer(serializers.ModelSerializer):
    stock_receipt = serializers.CharField(read_only=True)

    # product = ProductFormSerializer(read_only=True)
    product = ProductForeignKey()

    class Meta:
        model = StockProduct
        fields = [
            'id',
            'stock_receipt',
            'product',
            'quantity',
            'batch_number',
            'expire_date',
            'price',
        ]


class SalesmanForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return EmployeesProfile.objects.filter(distribution__user=self.context['request'].user)


class SalesInvoiceSerializer(serializers.ModelSerializer):
    salesman = SalesmanForeignKey()

    class Meta:
        model = SalesInvoice
        fields = [
            'invoice_number',
            'customer',
            'salesman',
            'discount',
            'customer_name',
            'customer_address',
            'customer_phone',
            'salesman_name',
            'discounted_price',
            'total_invoice_amount',
        ]


class StockProductForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        inventory = Inventory.objects.filter(distribution__user=user).first()

        if inventory:
            return StockProduct.objects.filter(stock_receipt__inventory=inventory)
        else:
            return StockProduct.objects.none()


class SalesProductSerializer(serializers.ModelSerializer):
    # stock_product = StockProductSerializer()

    stock_product = StockProductForeignKey()

    class Meta:
        model = SalesProduct
        fields = [
            'id',
            'stock_product',
            'quantity',
            'stock_product_name',
            'stock_product_batch',
            'stock_product_expire_date',
            'stock_product_price',
            'gross_price'
        ]


class InvoicesForeignKey(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        inventory = Inventory.objects.filter(distribution__user=user).first()

        if inventory:
            return StockProduct.objects.filter(stock_receipt__inventory=inventory)
        else:
            return StockProduct.objects.none()


class CustomerSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerSummary
        fields = [
            'id',
            'customer',
            'invoices',
            'total_paid',
            'total_debt'
        ]
