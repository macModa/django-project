from django.contrib import admin

from .models import *

admin.site.register(categorie)
admin.site.register(Produit)
admin.site.register(customer)
admin.site.register(Vente)
admin.site.register(facture_client)


# Register your models here.
