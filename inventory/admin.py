from django.contrib import admin

from .models import *


# Register your models here.

class StockReceiptInline(admin.TabularInline):
    model = StockReceipt


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = [
        'distribution',
        'timestamp'
    ]
    inlines = [StockReceiptInline]


class StockProductInline(admin.TabularInline):
    model = StockProduct


@admin.register(StockReceipt)
class StockReceiptAdmin(admin.ModelAdmin):
    list_display = [
        'inventory',
        'invoice_number',
        'company',
        'total_price',
        'discount',
        'discounted_price',
        'timestamp'
    ]
    inlines = [StockProductInline]


@admin.register(StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    list_display = [
        'stock_receipt',
        'product',
        'quantity',
        'batch_number',
        'expire_date',
        'price',
        'net_price',
        'timestamp'
    ]


class SalesProductInline(admin.TabularInline):
    model = SalesProduct


@admin.register(SalesInvoice)
class SalesInvoiceAdmin(admin.ModelAdmin):
    list_display = [
        'invoice_number',
        'customer',
        'customer_address',
        'salesman',
        'discount',
        'discounted_price',
        'total_invoice_amount',
        'invoice_date'
    ]
    inlines = [SalesProductInline]


@admin.register(SalesProduct)
class SalesProductAdmin(admin.ModelAdmin):
    list_display = [
        'invoice',
        'stock_product_name',
        'id',
        'quantity',
        'stock_product_batch',
        'stock_product_expire_date',
        'stock_product_price',
        'gross_price'
    ]


@admin.register(CustomerSummary)
class CustomerSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'inventory',
        'customer',
        'total_paid',
        'total_debt',
        'timestamp',

    ]
