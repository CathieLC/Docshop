from django.db import models
from django.urls import reverse

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


