from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import *


class InventoryViewSet(ModelViewSet):
   serializer_class = InventorySerializer
   permission_classes = [IsAuthenticated]
   queryset = Inventory.objects.all().select_related('distribution__user')

   @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
   def me(self, request):
      distribution_id = self.get_distribution_id(request.user)
      if not distribution_id:
         raise ValidationError('Invalid distribution ID')

      m = request.user
      inventory, created = Inventory.objects.get_or_create(distribution_id=distribution_id)
      if request.method == "GET":
         serializer = InventorySerializer(inventory)
         return Response(serializer.data)

   def get_distribution_id(self, user):
      try:
         distribution_profile = DistributionProfile.objects.get(user=user)
         return distribution_profile.id
      except DistributionProfile.DoesNotExist:
         return None


class StockReceiptViewSet(ModelViewSet):
   serializer_class = StockReceiptSerializer
   permission_classes = [IsAuthenticated]  # Adjust permissions as needed

   def perform_create(self, serializer):
      # Create a new StockReceipt instance, filtering the 'company' field choices based on the user
      stock_receipt = serializer.save(inventory=self.get_user_inventory())

   def get_queryset(self):
      # Filter the queryset to only include employees of the authenticated user's distribution
      return StockReceipt.objects.filter(inventory=self.get_user_inventory()) \
         .prefetch_related('stockproduct_set__product__company')

   def get_user_inventory(self):
      distribution_id = get_object_or_404(DistributionProfile, user=self.request.user)
      return get_object_or_404(Inventory, distribution_id=distribution_id)


class StockProductViewSet(ModelViewSet):
   serializer_class = StockProductSerializer
   permission_classes = [IsAuthenticated]  # Adjust permissions as needed

   def perform_create(self, serializer):
      stock_receipt = self.get_inventory_stock_receipt()  # Get the StockReceipt instance
      serializer.save(stock_receipt=stock_receipt)

   def get_queryset(self):
      return StockProduct.objects.filter(
         stock_receipt_id=self.get_inventory_stock_receipt().id
      ).select_related(
         'product__company', 'stock_receipt__inventory', 'stock_receipt__company__distribution'
      )

   def get_inventory_stock_receipt(self):
      stock_receipt_id = self.kwargs.get('stock_receipt_pk')
      inventory_id = Inventory.objects.filter(distribution_id__user=self.request.user).first()

      if not inventory_id:
         raise Http404("Inventory not found")

      return get_object_or_404(StockReceipt, inventory_id=inventory_id, id=stock_receipt_id)


class SalesInvoiceViewSet(ModelViewSet):
   serializer_class = SalesInvoiceSerializer
   permission_classes = [IsAuthenticated]  # Adjust permissions as needed

   def perform_create(self, serializer):
      # Assign the distribution profile to the employee being created
      sales_invoice = serializer.save(inventory=self.get_user_inventory())

      # Check if the customer name is provided in the request data
      customer_name = self.request.data.get('customer', None)

      if customer_name:
         # Update or create the CustomerSummary
         customer_summary, created = CustomerSummary.objects.get_or_create(
            inventory=sales_invoice.inventory,
            customer__name=customer_name,
            defaults={
               'inventory': sales_invoice.inventory,
               'customer': sales_invoice.customer,
               'total_paid': sales_invoice.total_paid,
               'total_debt': sales_invoice.total_invoice_amount - sales_invoice.total_paid
            }
         )

         # Update the existing CustomerSummary
         if not created:
            customer_summary.total_paid += sales_invoice.total_invoice_amount
            customer_summary.total_debt += (sales_invoice.total_invoice_amount - sales_invoice.total_paid)
            customer_summary.save()

         # Add the SalesInvoice to the many-to-many relationship
         customer_summary.invoices.add(sales_invoice)

      return Response(serializer.data, status=status.HTTP_201_CREATED)

   def get_queryset(self):
      # Filter the queryset to only include employees of the authenticated user's distribution
      return (
         SalesInvoice.objects.filter(
            inventory=self.get_user_inventory()
         )
         .select_related(
            'customer__district__province',
            'customer__sub_area__area',
            'salesman__distribution',
            'customer__area'
         )
         .prefetch_related(
            'salesproduct_set__stock_product__product'
         )
      )

   def get_user_inventory(self):
      distribution_profile = get_object_or_404(DistributionProfile, user=self.request.user)
      return get_object_or_404(Inventory, distribution_id=distribution_profile)


class SalesProductViewSet(ModelViewSet):
   serializer_class = SalesProductSerializer
   permission_classes = [IsAuthenticated]  # Adjust permissions as needed

   def perform_create(self, serializer):
      serializer.save(invoice=self.get_inventory_invoice())

   def get_queryset(self):
      return SalesProduct.objects.select_related('stock_product').filter(invoice=self.get_inventory_invoice())

   def get_inventory_invoice(self):
      distribution_id = get_object_or_404(DistributionProfile, user=self.request.user)
      inventory_id = get_object_or_404(Inventory, distribution_id=distribution_id)
      invoice_id = self.kwargs.get('invoice_pk')

      return get_object_or_404(SalesInvoice, inventory_id=inventory_id, id=invoice_id)


class CustomerSummaryViewSet(ModelViewSet):
   serializer_class = CustomerSummarySerializer
   permission_classes = [IsAuthenticated]  # Adjust permissions as needed

   def perform_create(self, serializer):
      serializer.save(inventory=self.get_user_inventory())

   def get_queryset(self):
      return CustomerSummary.objects.filter(inventory=self.get_user_inventory())

   def get_user_inventory(self):
      distribution_id = get_object_or_404(DistributionProfile, user=self.request.user)
      return get_object_or_404(Inventory, distribution_id=distribution_id)
