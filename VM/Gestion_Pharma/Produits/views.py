from django.shortcuts import render, redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib import messages
from django.views.generic import CreateView, DetailView
from .form import AjoutProduitform
from django.urls import path
import datetime
from .models import Produit,categorie







class Affichage(ListView):
    template_name = 'home.html'
    queryset = Produit.objects.all()
    
class AjoutProduit(CreateView):
    model = Produit
    form_class = AjoutProduitform
    template_name = 'ajout_donnees.html'
    success_url = reverse_lazy('home')
  
def ajout_donnees(request):
    # Initialize variables with default values
    errors = {}
    categorie = categorie.objects.all()
    price = None
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price_str = request.POST.get('price')  # Get as string
        quantite_str = request.POST.get('quantite')  # Get as string
        image = request.FILES.get('image')
        cat_id = request.POST.get('categorie')
        
        # Initialize variables
        price = None
        quantite = None
        cat_instance = None
        
        # Validate price
        try:
            price = float(price_str) if price_str else None
            if price is not None and price < 0:
                errors['price'] = "Le prix ne peut pas être négatif."
        except (ValueError, TypeError):
            errors['price'] = "Le prix doit être un nombre valide."
        
        # Validate quantity
        try:
            quantite = int(quantite_str) if quantite_str else None
            if quantite is not None and quantite < 0:
                errors['quantite'] = "La quantité ne peut pas être négative."
        except (ValueError, TypeError):
            errors['quantite'] = "La quantité doit être un nombre entier valide."
        
        # Validate category
        try:
            cat_instance = categorie.objects.get(pk=cat_id) if cat_id else None
        except (categorie.DoesNotExist, ValueError):
            errors['categorie'] = "La catégorie sélectionnée n'existe pas."
        
        # Only proceed if no validation errors
        if not errors:
            try:
                # Create and save product
                produit = Produit(
                    name=name,
                    description=description,
                    price=price,
                    quantite=quantite,
                    image=image,
                    categorie=cat_instance
                )
                produit.save()
                messages.success(request, "Produit ajouté avec succès.")
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'ajout du produit : {str(e)}")
    
    # Always render the template with categories
    return render(request, 'ajout_donnees.html', {
        "categorie": categorie,
        "errors": errors
    })
    
    
def modifier_donnees(request, pk):
    all_categorie = categorie.objects.all()
    produit = get_object_or_404(Produit, pk=pk)  # Déplacé en HAUT de la fonction
    errors = {}
    if request.method == 'POST':
        form = AjoutProduitform(request.POST, request.FILES, instance=produit)
        
       
       
       
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès.")
            return redirect('home')
        else:
            # Form has errors - they'll be displayed in template automatically
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        
        
        # If form is not valid, continue to manual validation below
        name = request.POST.get('name')
        description = request.POST.get('description')
        price_str = request.POST.get('price')
        quantite_str = request.POST.get('quantite')
        image = request.FILES.get('image')
        cat_id = request.POST.get('categorie')
        date_expiration = request.POST.get('date_expiration', None)

        
        # validate des champs
        if not name:
            errors['name'] = "Le nom du produit est obligatoire."
        if not description:
            errors['description'] = "La description du produit est obligatoire."
        if not price_str:
            errors['price'] = "Le prix du produit est obligatoire."
        if not quantite_str:
            errors['quantite'] = "La quantité du produit est obligatoire."
        if not cat_id:
            errors['categorie'] = "La catégorie du produit est obligatoire."
        if date_expiration:
            try:
                date_expiration = datetime.datetime.strptime(date_expiration, '%Y-%m-%d').date()
            except ValueError:
                errors['date_expiration'] = "La date d'expiration doit être au format YYYY-MM-DD."
        if not errors:
            try:
                # Update product
                cat_instance = categorie.objects.get(id=cat_id)
                produit.name = name
                produit.description = description
                produit.price = float(price_str)
                produit.quantite = int(quantite_str)
                produit.categorie = cat_instance
                produit.date_expiration = date_expiration if date_expiration else produit.date_expiration
                if image:
                    fs = FileSystemStorage()
                    filename = fs.save(image.name, image)
                    produit.image = filename
            except ValueError:
                errors['categorie'] = "La catégorie sélectionnée n'existe pas."
        
        produit.save()
        messages.success(request, "Produit modifié avec succès.")
        return redirect('home')
    else:
        # GET request - initialize form with product instance
        form = AjoutProduitform(instance=produit)
    
    return render(request, 'modifier_donnees.html', {
        'form': form,
        'produit': produit,
        'categories': all_categorie,
        'errors': errors})
                
           
            
   # fonction suprimer
def suprimer(request, pk):
    try:
        produit = get_object_or_404(Produit, pk=pk)
        if request.method == 'POST':
            produit.delete()
            return JsonResponse({'success': True, 'message': 'Produit supprimé avec succès'})
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'}, status=405)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
    
def detail(request, pk):
    # Récupérer le produit ou renvoyer une 404 si non trouvé
    produit = Produit.objects.get( pk=pk)
    return render(request, 'detail.html', {'produit': produit})
from django.shortcuts import render
from .models import Produit  # Remplacez par votre modèle

from django.shortcuts import render
from .models import Produit

def recherche(request):
    query = request.GET.get('q','').strip()
    

        # Comportement alternatif lorsque la recherche est vide :
    donnees = Produit.objects.all()
    if query:
        donnees = Produit.objects.filter(name__icontains=query)
    
        
    context = {
        
        'donnees': donnees,
        'query': query,
    }
    
    return render(request, 'resultat_recherche.html', context)


   
   