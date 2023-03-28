from django.shortcuts import render
from store.models import Product

def index(request):
    produits = Product.objects.all()
    return render(request, 'store/index.html', context={"produits":produits})
