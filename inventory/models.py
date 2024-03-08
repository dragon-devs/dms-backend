from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

user = 9


class Inventory(models.Model):
    distribution = models.OneToOneField('distribution.DistributionProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.distribution.name} INVENTORY"


class StockReceipt(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    company = models.ForeignKey('distribution.CompanyProfile', on_delete=models.CASCADE)
    discount = models.FloatField(default=10.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def discounted_price(self):
        return self.total_price - (self.total_price * (self.discount / 100))

    @property
    def total_price(self):
        total_net_price = sum(stock_product.net_price for stock_product in self.stockproduct_set.all())
        return total_net_price

    @property
    def invoice_number(self):
        if self.id:
            return f"#{str(self.id).zfill(4)}"
        else:
            return None

    def __str__(self):
        return f"{self.invoice_number} : {self.company.name}"


class StockProduct(models.Model):
    stock_receipt = models.ForeignKey(StockReceipt, on_delete=models.CASCADE)
    product = models.ForeignKey('distribution.ProductForm', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    batch_number = models.CharField(max_length=10, unique=True)
    expire_date = models.DateField()
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.company.name} : {self.product.name} : #{self.batch_number}"


    @property
    def net_price(self):
        net_price = self.quantity * self.price
        return net_price


class SalesInvoice(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    salesman = models.ForeignKey('distribution.EmployeesProfile', on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(default=10.0)
    total_paid = models.FloatField(default=0.0)
    total_invoice_amount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if self.pk:
            # Calculate total_invoice_amount for a new instance
            self.total_invoice_amount = self.calculate_total_invoice_amount()
        super().save(*args, **kwargs)

    def calculate_total_invoice_amount(self):
        sales_products = self.salesproduct_set.all()
        if sales_products:
            return sum(sales_product.gross_price for sales_product in sales_products)
        else:
            return 0.0

    @property
    def invoice_number(self):
        if self.id:
            return f"#{str(self.id).zfill(4)}"
        else:
            return None

    @property
    def summary_number(self):
        if self.customer.id:
            return f"#{str(self.customer.id).zfill(4)}"
        else:
            return None

    @property
    def customer_name(self):
        if self.customer:
            return self.customer.name
        else:
            return None

    @property
    def customer_address(self):
        if self.customer:
            return self.customer.address
        else:
            return

    @property
    def customer_phone(self):
        if self.customer:
            return self.customer.phone
        else:
            return None

    @property
    def salesman_name(self):
        if self.salesman:
            return self.salesman.name
        else:
            return None

    @property
    def salesman_phone(self):
        if self.salesman:
            return self.salesman.phone
        else:
            return None

    @property
    def discounted_price(self):
        total_amount = self.total_invoice_amount
        if total_amount is not None:
            return total_amount - (total_amount * (self.discount / 100))
        else:
            return None  # Or any other default value you prefer

    def __str__(self):
        return f"{self.invoice_number} : {self.customer.name}"


class SalesProduct(models.Model):
    invoice = models.ForeignKey(SalesInvoice, on_delete=models.CASCADE)
    stock_product = models.ForeignKey(StockProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    original_quantity_sold = models.IntegerField(default=0)

    # Other SalesProduct fields and methods
    def __str__(self):
        return f"{self.stock_product_name} : {self.invoice.customer_name}"

    def save(self, *args, **kwargs):
        invoice = self.invoice  # Get the associated SalesInvoice

        if invoice:
            if not self.pk:
                # New SalesProduct: Subtract from StockProduct
                self._subtract_from_stock(self.quantity)
            else:
                # Updated SalesProduct: Check if quantity changed
                old_sales_product = SalesProduct.objects.get(pk=self.pk)
                if self.quantity != old_sales_product.quantity:
                    difference = self.quantity - old_sales_product.quantity
                    self._subtract_from_stock(difference)

        super().save(*args, **kwargs)  # Call the original save method

        if invoice:
            # Recalculate the total_invoice_amount for the associated invoice
            total_amount = sum(sales_product.gross_price for sales_product in invoice.salesproduct_set.all())
            invoice.total_invoice_amount = total_amount
            invoice.save()

    def delete(self, *args, **kwargs):
        invoice = self.invoice  # Get the associated SalesInvoice
        stock_product = self.stock_product  # Get the associated StockProduct
        super().delete(*args, **kwargs)  # Call the original delete method

        if invoice:
            # Update the associated invoice's total_invoice_amount
            total_amount = sum(sales_product.gross_price for sales_product in invoice.salesproduct_set.all())
            invoice.total_invoice_amount = total_amount
            invoice.save()

        if stock_product:
            # Add the quantity back to StockProduct
            stock_product.quantity += self.quantity
            stock_product.save()

    def _subtract_from_stock(self, quantity_to_subtract):
        if self.stock_product:
            if quantity_to_subtract > self.stock_product.quantity:
                raise ValidationError("Quantity exceeds available stock product quantity.")
            self.stock_product.quantity -= quantity_to_subtract
            self.stock_product.save()

    def _add_to_stock(self, quantity_to_add):
        if self.stock_product:
            self.stock_product.quantity += quantity_to_add
            self.stock_product.save()

    @property
    def stock_product_name(self):
        if self.stock_product:
            return self.stock_product.product.name
        else:
            return None

    @property
    def stock_product_batch(self):
        if self.stock_product:
            return self.stock_product.batch_number
        else:
            return None

    @property
    def stock_product_expire_date(self):
        if self.stock_product:
            return self.stock_product.expire_date
        else:
            return None

    @property
    def stock_product_price(self):
        if self.stock_product:
            return self.stock_product.price
        else:
            return None

    @property
    def gross_price(self):
        if self.stock_product:
            return self.stock_product.price * self.quantity
        else:
            return None


class CustomerSummary(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    customer = models.OneToOneField('customer.Customer', on_delete=models.CASCADE)
    invoices = models.ManyToManyField(SalesInvoice, null=True, blank=True)
    total_paid = models.FloatField(default=0.0, null=True)
    total_debt = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Summary : {self.customer.name}"

    def save(self, *args, **kwargs):
        # Add all related SalesInvoice instances to the invoices field
        self.invoices.set(self.customer.salesinvoice_set.all())

        # Calculate the total paid amount by summing the 'total_invoice_amount' field from related invoices
        self.total_paid = self.invoices.aggregate(total_amount=Sum('total_invoice_amount'))['total_amount'] or 0.0

        # Calculate the total debt as the difference between the total invoice amount and total paid amount
        total_invoice_amount = self.invoices.aggregate(total_amount=Sum('total_invoice_amount'))[
                                   'total_amount'] or 0.0
        self.total_debt = total_invoice_amount - self.total_paid

        super().save(*args, **kwargs)

