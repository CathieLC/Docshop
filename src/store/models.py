from django.db import models
from django.urls import reverse
from django.utils import timezone

from shop.settings import AUTH_USER_MODEL

"""
- Nom (text)
- Prix (float)
- Quantité en stock pour un produit donné (int)
- Description (text)
- Image du produit
-Après coup je rajoute un champ slug de type slugfield
"""


class Product(models.Model):
    name = models.CharField(max_length=130)
    slug = models.SlugField(max_length=130)
    price = models.FloatField(default=0.0)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="products", blank=True, null=True) #nom du dossier où seront stockées les images, null est obligatoire si blank est présent.

    def __str__(self):
        return f"{self.name} ({self.stock} en stock)" # on veut le nom de l'article et le nombre en stock

    def get_absolute_url(self): # va me rajouter un boutons dans admin/products/nom du produit => Voir sur le site
        return reverse("products", kwargs={"slug": self.slug})


#Articles (Order)
"""
- Utilisateur (foreignkey & plusieurs articles vont être relié à un utilisateur)
- Produit
- Quantité
- Commandé ou non
"""

class Order(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) # Si l'utilisateur supprime son compte les articles liés à cet utilisateur seront supprimés aussi
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False) #par défaut l'article n'auras pas été commandé
    ordered_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


#Panier (Cart)
"""
- Utilisateur (one to one car un utilisateur ne peut avoir qu'un seul panier
- Articles du panier (on pa plusieurs articles qui peuvent être ajoutés)
- Quantité
- Commandé ou non
- Date de la commande
"""

class Cart(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    orders = models.ManyToManyField(Order)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        for order in self.orders.all():
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()

        self.orders.clear()
        super().delete(*args, **kwargs)