from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from store.views import index, product_detail, add_to_cart, remove_to_cart, cart, delete_cart
from shop import settings
from accounts.views import signup, logout_user, login_user

from views.views import home

urlpatterns = [

    path('', home, name='home'),
    path('index', index, name='index'),
    path("admin/", admin.site.urls),
    path("signup", signup, name="signup"),
    path("login", login_user, name="login"),
    path("logout", logout_user, name="logout"),

    path("product/<str:slug>/", product_detail, name="products"),
    path("product/<str:slug>/add-to-cart/", add_to_cart, name="add-to-cart"),
    path("product/<str:slug>/remove_to_cart/", remove_to_cart, name="remove-to-cart"),

    path("cart", cart, name="cart"),
    path("cart/delete", delete_cart, name="delete-cart"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
