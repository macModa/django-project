from django.db import models
class categorie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
# Class pour les produits
class Produit(models.Model):
    name = models.CharField(max_length=100, unique=True)
    categorie = models.ForeignKey(categorie, on_delete=models.CASCADE, related_name='produits')
    price = models.IntegerField()
    quantite = models.PositiveBigIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='media/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['date_ajout']
        
    def statut_quantite(self):
         # quantite =0 affiche rouge
         if self.quantite == 0:
             return 'red'
         elif self.quantite <= 10:
             return 'orange'
             
         elif self.quantite > 10:
             return 'green' 
         
         
    def __str__(self):
        return self.name         
class customer(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
        
                  
class Vente(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, )
    quantite = models.PositiveBigIntegerField(default=0)
    date_vente = models.DateTimeField(auto_now_add=True)
    customer = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"{self.produit.name} - {self.quantite} unités"

    class Meta:
        ordering = ['date_vente']
        
class facture_client(models.Model):
        customer = models.ForeignKey(customer, on_delete=models.CASCADE)
        quantite = models.PositiveBigIntegerField(default=0)
        date_achat = models.DateTimeField(auto_now_add=True)
        total_amount = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='factures')
       
       

        def __str__(self):
            return f"Facture {self.id} - {self.vente.produit.name}"
        
        