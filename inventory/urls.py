from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import InventoryViewSet, StockReceiptViewSet, StockProductViewSet, SalesInvoiceViewSet, SalesProductViewSet, \
    CustomerSummaryViewSet

router = DefaultRouter()
router.register(r'inventory', InventoryViewSet, basename='inventory')

inventory_router = NestedDefaultRouter(router, r'inventory', lookup='inventory')
inventory_router.register(r'stock-receipts', StockReceiptViewSet, basename="inventory-receipts")
inventory_router.register(r'invoices', SalesInvoiceViewSet, basename="inventory-invoices")
inventory_router.register(r'summary', CustomerSummaryViewSet, basename="customer-summary")

stock_receipt_router = NestedDefaultRouter(inventory_router, r'stock-receipts', lookup='stock_receipt')
stock_receipt_router.register(r'products', StockProductViewSet, basename="inventory-products")

invoice_router = NestedDefaultRouter(inventory_router, r'invoices', lookup='invoice')
invoice_router.register(r'products', SalesProductViewSet, basename="invoice-products")

urlpatterns = [
    path('inventory/', RedirectView.as_view(url='/inventory/me/')),
    path('', include(router.urls)),
    path('', include(inventory_router.urls)),
    path('', include(stock_receipt_router.urls), name='stock-receipts-products'),  # Adjust the name
    path('', include(invoice_router.urls), name='invoice-products'),  # Adjust the name
]
