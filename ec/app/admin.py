from django.contrib import admin
from . models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','precio_descuento','categoria','imagen_producto']
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin): 
    list_display = ['id','user','localidad','departamento','codigopostal']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'productos', 'cantidad']
    def productos(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
    
@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','productos','cantidad','ordered_date','status','payment']
    def customers(self,obj):
        link = reverse("admin:app_customer_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product)
    
    def productos(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
    def payments(self,obj):
        link = reverse("admin:app_payment_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)
    
    
    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','productos']
    def productos(self,obj):
        link = reverse("admin:app_product_change",args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>',link,obj.product.title)
    
    
admin.site.unregister(Group)
    

