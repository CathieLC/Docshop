from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from store.models import Product

def index(request):
    produits = Product.objects.all()
    return render(request, 'store/index.html', context={"produits":produits})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug) # en rouge c'est le champs de la table, et ce qu'on lui passe c'est ce qu'on récupère dans la fonction
    return render(request, "store/detail.html", context={"product_detail": product})

