from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view

from . import views
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, CustomerRegistrationForm


# ----------------------------
# Logout personalizado
# ----------------------------
class MyLogoutView(auth_view.LogoutView):
    http_method_names = ['get', 'post']


# ----------------------------
# URL patterns principales
# ----------------------------
urlpatterns = [
    # Página de inicio y páginas informativas
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),

    # Categorías y productos
    path("categoria/<slug:val>", views.CategoryView.as_view(), name="categoria"),
    path("categoria-title/<val>", views.CategoryTitle.as_view(), name="categoria-title"),
    path("product-detail/<int:pk>", views.ProductDetail.as_view(), name="product-detail"),

    # Carrito y wishlist
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('wishlist/', views.show_wishlist, name='showwishlist'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),

    # Direcciones del usuario
    path('address/', views.address, name='address'),
    path('updateAddress/<int:pk>', views.UpdateAddress.as_view(), name='updateAddress'),
    path('address/delete/<int:pk>/', views.delete_address, name='delete_address'),
    path('address/set-default/<int:pk>/', views.set_default_address, name='set_default_address'),

    # Checkout y pagos
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('api/save-payment/', views.save_payment, name='save-payment'),
    path('payment/success/', views.payment_success, name='payment_success'),

    # Órdenes
    path('orders/', views.orders, name='orders'),

    # Busqueda
    path('search/', views.search, name='search'),

    # Registro y perfil de usuario
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('profile/', views.ProfileView.as_view(), name='profile'),

    # Autenticación / login / logout / contraseñas
    path('accounts/login/', auth_view.LoginView.as_view(
        template_name='app/login.html', 
        authentication_form=LoginForm
    ), name='login'),

    path('logout/', MyLogoutView.as_view(next_page='login'), name="logout"),

    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='app/password_reset.html',
        form_class=MyPasswordResetForm
    ), name='password_reset'),

    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='app/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='app/password_reset_confirm.html',
        form_class=MyPasswordChangeForm
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='app/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('passwordchange/', auth_view.PasswordChangeView.as_view(
        template_name='app/changepassword.html',
        form_class=MyPasswordChangeForm,
        success_url='/passwordchangedone'
    ), name='passwordchange'),

    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(
        template_name='app/passwordchangedone.html'
    ), name='passwordchangedone'),
]

# Archivos estáticos / media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ----------------------------
# Configuración del admin
# ----------------------------
admin.site.site_header = "Ecommerce"
admin.site.site_title = "Ecommerce"
admin.site.site_index_title = "Bienvenido a Minino tecs"