from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . models import Customer, Product, Cart, Payment, OrderPlaced, Wishlist
from django.contrib.auth.models import Group
# Register your models here.


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'subtitle',
                    'discount_price', 'category', 'product_image']


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'nation', 'region', 'district', 'zipcode']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id',
                    'razorpay_payment_status', 'razorpay_payment_id', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer',
                    'product', 'quantity', 'ordered_date', 'status', 'payment']


@admin.register(Wishlist)
class WishlistModalAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']

    def products(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


admin.site.unregister(Group)
