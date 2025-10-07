from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

from .models import Cart, OrderPlaced, Product, Customer, Wishlist, Payment
from .forms import CustomerProfileForm, CustomerRegistrationForm


# -----------------------------
# Helper functions
# -----------------------------

def get_cart_and_wishlist_counts(user):
    """Retorna la cantidad de items en carrito y wishlist para el usuario"""
    if user.is_authenticated:
        totalitem = Cart.objects.filter(user=user).count()
        wishitem = Wishlist.objects.filter(user=user).count()
    else:
        totalitem = 0
        wishitem = 0
    return totalitem, wishitem


def clear_cart(user):
    """Elimina todos los productos del carrito del usuario"""
    Cart.objects.filter(user=user).delete()


# -----------------------------
# Vistas Generales
# -----------------------------

def home(request):
    """Vista de la página de inicio"""
    productos = [
        {'url': 'NK', 'img': 'z2.png', 'nombre': 'Zapatos Nike'},
        {'url': 'AD', 'img': 'za1.png', 'nombre': 'Zapatos Adidas'},
        {'url': 'CA', 'img': 'ca4.png', 'nombre': 'Camisas'},
        {'url': 'CO', 'img': 'c1.png', 'nombre': 'Conjuntos'},
        {'url': 'PA', 'img': 'p1.png', 'nombre': 'Pantalones'},
        {'url': 'GO', 'img': 'gorra1.png', 'nombre': 'Gorras'},
    ]
    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    context = {'productos': productos, 'totalitem': totalitem, 'wishitem': wishitem}
    return render(request, "app/home.html", context)


def about(request):
    """Vista de la página 'About'"""
    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    return render(request, "app/about.html", {'totalitem': totalitem, 'wishitem': wishitem})


def contact(request):
    """Vista de la página de contacto"""
    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    return render(request, "app/contact.html", {'totalitem': totalitem, 'wishitem': wishitem})


# -----------------------------
# Vistas de Productos y Categorías
# -----------------------------

class CategoryView(View):
    """Vista de categoría por slug"""
    def get(self, request, val):
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        product = Product.objects.filter(categoria=val)
        title = Product.objects.filter(categoria=val).values('title')
        return render(request, "app/categoria.html", locals())


class CategoryTitle(View):
    """Vista de categoría filtrando por título de producto"""
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(categoria=product[0].categoria).values('title')
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        return render(request, "app/categoria.html", locals())


class ProductDetail(View):
    """Detalle de un producto individual"""
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        wishlist = False
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        context = {
            "product": product,
            "wishlist": wishlist,
            "totalitem": totalitem,
            "wishitem": wishitem,
        }
        return render(request, "app/productdetail.html", context)


# -----------------------------
# Vistas de Registro y Perfil
# -----------------------------

class CustomerRegistrationView(View):
    """Registro de usuarios"""
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        return render(request, 'app/customerregistration.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Usuario registrado con éxito!")
            return redirect('login')
        else:
            messages.warning(request, "Datos inválidos. Verifica los campos.")
        return render(request, 'app/customerregistration.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})


class ProfileView(View):
    """Perfil de usuario"""
    @method_decorator(login_required)
    def get(self, request):
        form = CustomerProfileForm()
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        return render(request, 'app/profile.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})

    @method_decorator(login_required)
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        if form.is_valid():
            Customer.objects.update_or_create(
                user=request.user,
                defaults={
                    'name': form.cleaned_data['name'],
                    'localidad': form.cleaned_data['localidad'],
                    'departamento': form.cleaned_data['departamento'],
                    'mobile': form.cleaned_data['mobile'],
                    'codigopostal': form.cleaned_data['codigopostal'],
                }
            )
            messages.success(request, "Perfil guardado correctamente")
            return redirect('profile')
        messages.warning(request, "Datos inválidos")
        return render(request, 'app/profile.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})


# -----------------------------
# Vistas de Dirección
# -----------------------------

@login_required
def address(request):
    """Muestra y agrega direcciones del usuario"""
    add = Customer.objects.filter(user=request.user)
    form = CustomerProfileForm()
    show_form = False

    if request.method == "POST":
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, "Dirección agregada correctamente")
            return redirect('address')
        else:
            show_form = True  # si hay errores, mantener el formulario abierto

    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    context = {'add': add, 'form': form, 'show_form': show_form, 'totalitem': totalitem, 'wishitem': wishitem}
    return render(request, 'app/address.html', context)


@login_required
def set_default_address(request, pk):
    """Marca una dirección como predeterminada"""
    Customer.objects.filter(user=request.user).update(is_default=False)
    ad = get_object_or_404(Customer, pk=pk, user=request.user)
    ad.is_default = True
    ad.save()
    messages.success(request, "Dirección establecida como predeterminada")
    return redirect('address')


@login_required
def delete_address(request, pk):
    """Elimina una dirección"""
    ad = get_object_or_404(Customer, pk=pk, user=request.user)
    ad.delete()
    messages.success(request, "Dirección eliminada correctamente")
    return redirect('address')


@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    """Actualizar dirección existente"""
    def get(self, request, pk):
        add = get_object_or_404(Customer, pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
        return render(request, 'app/updateAddress.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem, 'add': add})

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = get_object_or_404(Customer, pk=pk)
            add.name = form.cleaned_data['name']
            add.localidad = form.cleaned_data['localidad']
            add.departamento = form.cleaned_data['departamento']
            add.mobile = form.cleaned_data['mobile']
            add.codigopostal = form.cleaned_data['codigopostal']
            add.save()
            messages.success(request, "Felicidades! Perfil Actualizado")
        else:
            messages.warning(request, "Datos inválidos")
        return redirect("address")


# -----------------------------
# Vistas de Carrito y Wishlist
# -----------------------------

@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value= p.cantidad * p.product.precio_descuento
        amount = amount + value
    totalamount = amount + 40
    totalitem= 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem= 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user = user)
    return render(request, "app/wishlist.html",locals())


# -----------------------------
# Vistas de Checkout y Pagos
# -----------------------------

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    """Vista de Checkout"""
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)

        # Revisar si se pasa un producto para "Comprar Ahora"
        prod_id = request.GET.get('prod_id')
        if prod_id:
            product = get_object_or_404(Product, id=prod_id)
            cart_items = [{'product': product, 'cantidad': 1}]
            famount = product.precio_descuento
        else:
            cart_items = Cart.objects.filter(user=user)
            famount = sum(p.cantidad * p.product.precio_descuento for p in cart_items)

        totalamount_num = famount + 40
        totalamount = f"{totalamount_num:.2f}"
        razoraumont = int(totalamount_num * 100)

        totalitem, wishitem = get_cart_and_wishlist_counts(user)
        context = {
            "totalitem": totalitem,
            "wishitem": wishitem,
            "user": user,
            "add": add,
            "cart_items": cart_items,
            "famount": famount,
            "totalamount": totalamount,
            "totalamount_num": totalamount_num,
            "razoraumont": razoraumont,
        }
        return render(request, 'app/checkout.html', context)


@login_required
def payment_success(request):
    """Página de éxito de pago"""
    clear_cart(request.user)
    return render(request, 'app/payment_success.html')


@csrf_exempt
@login_required
def save_payment(request):
    """Guardar pago desde PayPal (API)"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user

            # Guardar pago
            payment = Payment.objects.create(
                user=user,
                order_id=data['id'],
                payment_id=data['id'],
                payer_email=data['payer']['email_address'],
                amount=data['purchase_units'][0]['amount']['value'],
                status=data['status'],
                paid=True
            )

            # Obtener dirección seleccionada
            customer_id = data.get('customer_id')
            customer = Customer.objects.get(pk=customer_id) if customer_id else Customer.objects.filter(user=user).last()

            # Crear orden por cada producto en el carrito
            cart_items = Cart.objects.filter(user=user)
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=user,
                    customer=customer,
                    product=item.product,
                    cantidad=item.cantidad,
                    payment=payment,
                    status="Pending"
                )

            # Vaciar carrito
            cart_items.delete()
            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})


# -----------------------------
# Vistas de Órdenes
# -----------------------------

@login_required
def orders(request):
    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': order_placed, 'totalitem': totalitem, 'wishitem': wishitem})


# -----------------------------
# Vistas de manipulación de carrito vía AJAX
# -----------------------------

@login_required
def plus_cart(request):
    """Incrementar cantidad de un producto en el carrito"""
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)
        cart_item.cantidad += 1
        cart_item.save()

        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.cantidad * p.product.precio_descuento for p in cart)
        totalamount = amount + 40
        return JsonResponse({'cantidad': cart_item.cantidad, 'amount': amount, 'totalamount': totalamount})


@login_required
def minus_cart(request):
    """Disminuir cantidad de un producto en el carrito"""
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)
        if cart_item.cantidad > 1:
            cart_item.cantidad -= 1
            cart_item.save()

        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.cantidad * p.product.precio_descuento for p in cart)
        totalamount = amount + 40
        return JsonResponse({'cantidad': cart_item.cantidad, 'amount': amount, 'totalamount': totalamount})


@login_required
def remove_cart(request):
    """Eliminar un producto del carrito"""
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = get_object_or_404(Cart, product=prod_id, user=request.user)
        cart_item.delete()

        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.cantidad * p.product.precio_descuento for p in cart)
        totalamount = amount + 40
        return JsonResponse({'cantidad': 0, 'amount': amount, 'totalamount': totalamount})


# -----------------------------
# Vistas de Wishlist vía AJAX
# -----------------------------

@login_required
def plus_wishlist(request):
    """Agregar producto a wishlist"""
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        product = get_object_or_404(Product, id=prod_id)
        Wishlist.objects.get_or_create(user=request.user, product=product)
        return JsonResponse({"message": "Producto agregado a tu lista de deseos"})


@login_required
def minus_wishlist(request):
    """Eliminar producto de wishlist"""
    if request.method == "GET":
        prod_id = request.GET.get("prod_id")
        product = get_object_or_404(Product, id=prod_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        return JsonResponse({"message": "Producto eliminado de tu lista de deseos"})


# -----------------------------
# Vista de búsqueda
# -----------------------------

def search(request):
    """Buscar productos por título"""
    query = request.GET.get('search', '')
    totalitem, wishitem = get_cart_and_wishlist_counts(request.user)
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, "app/search.html", {'product': product, 'totalitem': totalitem, 'wishitem': wishitem})