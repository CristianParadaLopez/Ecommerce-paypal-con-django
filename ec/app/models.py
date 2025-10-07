from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
# Create your models here.

STATE_CHOICES = (
    ('AH', 'Ahuachapán'),
    ('CA', 'Cabañas'),
    ('CH', 'Chalatenango'),
    ('CU', 'Cuscatlán'),
    ('LI', 'La Libertad'),
    ('PA', 'La Paz'),
    ('UN', 'La Unión'),
    ('MO', 'Morazán'),
    ('SM', 'San Miguel'),
    ('SS', 'San Salvador'),
    ('SV', 'San Vicente'),
    ('SA', 'Santa Ana'),
    ('SO', 'Sonsonate'),
    ('US', 'Usulután'),
)


CATEGORY_CHOICES=(
    ('AD','Adidas'),
    ('NK','NIKE'),
    ('CA','Camisas'),
    ('CO','Conjuntos'),
    ('PA','Pantalones'),
    ('GO','Gorras'),

)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    precio_descuento = models.FloatField()
    description = models.TextField()
    categoria = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    imagen_producto = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    localidad = models.CharField(max_length=200)
    departamento = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    codigopostal = models.IntegerField()
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.cantidad * self.product.precio_descuento
    
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Pacled'),
    ('On The Way', 'On The way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)    


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid = models.BooleanField(default=False)
    order_id = models.CharField(max_length=255, blank=True, null=True)    # ID de la orden de PayPal
    payment_id = models.CharField(max_length=255, blank=True, null=True)  # ID del pago de PayPal
    payer_email = models.EmailField(blank=True, null=True)                 # Email del comprador
    status = models.CharField(max_length=50, blank=True, null=True)        # Estado del pago ('COMPLETED', etc.)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} USD - {'✅' if self.paid else '❌'}"

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.cantidad * self.product.precio_descuento
    

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)