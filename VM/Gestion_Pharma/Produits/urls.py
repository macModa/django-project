from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
   
    path('', TemplateView.as_view(template_name="accueil.html"), name='accueil'),
    path('accueil/', TemplateView.as_view(template_name="accueil.html"), name='accueil'),
    path('produits/', Affichage.as_view(), name='produit'),
    path('ajout/', AjoutProduit.as_view(), name='ajout_produit'),
    #path('ajout/',ajout_donnees, name='ajout_donnees'),
    path('modifier/<int:pk>/',modifier_donnees, name='modifier_donnees'),
    path('suprimer/<int:pk>/', suprimer, name='suprimer_donnees'),
    path('detail/<int:pk>/', detail, name='detail'),
    path('recherche/', recherche, name='recherche'),
    path('ajoutVente/<int:id>/', VenteProduit, name='ajoutVente'),
    path('enregitrement-recu/<int:sale_id>/', facture, name='saverecu'),
    path('facture/<int:sale_id>/', Facture, name='facture'),
  ] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
