import time

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from store.models import Product, Cart, Order




def index(request):
    produits = Product.objects.all()
    return render(request, 'store/index.html', context={"produits":produits})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug) # en rouge c'est le champs de la table, et ce qu'on lui passe c'est ce qu'on récupère dans la fonction
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, "store/detail.html", context={"product_detail": product, "orders": cart.orders.all()})

"""
cas de figures :
- Utilisateur n'a pas encore de panier (il par de zéro)
- A déjà des articles dans son panier, l'article y est déjà, il faut changer la quantité (incrémenter de 1)

"""
def add_to_cart(request, slug):
    # on récupère simplement l'utilisateur
    user = request.user
    product = get_object_or_404(Product, slug=slug)

    # le _ est une variable nécessaire pour le get or create qui récupère deux objets mais par convention,
    # c'est une variable qui ne sera pas utlisée dans la suite de mon code
    cart, _ = Cart.objects.get_or_create(user=user) #si le panier n'existe pas il sera créé

    # order ce sera l'article à récupérer si il existe déjà dans le panier
    # created permettra à l'article d'être créé dans le panier si ce n'est pas le cas
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity +=1
        order.save()

    return redirect(reverse("products", kwargs={"slug": slug}))


#essai retrait du panier

def remove_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    cart, _ = Cart.objects.get_or_create(user=user)
    order, created = Order.objects.get_or_create(user=user,
                                                 ordered=False,
                                                 product=product)
    if created:
        cart.orders.add(order)
        cart.save()
    else:
        order.quantity -=1
        order.save()

    return redirect(reverse("products", kwargs={"slug": slug}))


#fin essai retrait du panier



def cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, "store/cart.html", context={"orders": cart.orders.all()})


#j'ai modifié le modèle et donc cette fonction n'est plus utile
# def delete_cart(request):
#     #je récupère le panier
#     cart = request.user.cart
#
#     if cart:
#         #si panier, je récupère tout puis le je le delete
#         cart.orders.all().delete()
#         cart.delete()
#
#     return redirect('index')


def delete_cart(request):
    #je récupère le panier
    cart = request.user.cart

    if cart:
        cart.delete()

    return redirect('index')


