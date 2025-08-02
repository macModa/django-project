from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages

import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User





# fonction cree un compte utilisateur
def Cration_Compte(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password_confirm']

        # Validation des champs
        if not username or not email or not password or not confirm_password:
            messages.error(request, "Tous les champs sont obligatoires")
            return redirect("creation")

        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return redirect("creation")
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[A-Z]', password):
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères, une majuscule et un chiffre")
            return redirect("creation")

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Adresse e-mail invalide")
            return redirect("creation")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Le nom d'utilisateur existe déjà")
            return redirect("creation")

        if User.objects.filter(email=email).exists():
            messages.error(request, "L'adresse e-mail est déjà utilisée")
            return redirect("creation")

        # Création de l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Compte créé avec succès")
        return redirect("login")

    return render(request, 'creation.html')



# Create your views here.
def connecter_compte(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, "Identifiants invalides")
            return redirect("login")

    return render(request, 'login.html')

def verification_Mail(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.error(request, "L'adresse e-mail est obligatoire")
            return render(request, 'verificationMail.html')
        
        user = User.objects.filter(email=email).first()
        if user:
            return redirect('changement_code', email=email)
        else:
            messages.error(request, "Aucun utilisateur trouvé avec cet e-mail.")
            return render(request, 'verificationMail.html')

    return render(request, 'verificationMail.html')

# fonction pour changer le mot passe apres verification de l'ancien mot de passe
def changement_code(request, email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, "Aucun utilisateur trouvé avec cet e-mail.")
        return redirect('verification')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation des champs
        if not password or not password_confirm:
            messages.error(request, "Tous les champs sont obligatoires")
            return render(request, 'nouveauMDP.html', {'email': email})
        
        # Vérification que les mots de passe correspondent
        if password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas")
            return render(request, 'nouveauMDP.html', {'email': email})
        
        # Validation de la complexité du mot de passe
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères")
            return render(request, 'nouveauMDP.html', {'email': email})
        
        if not re.search(r'\d', password):
            messages.error(request, "Le mot de passe doit contenir au moins un chiffre")
            return render(request, 'nouveauMDP.html', {'email': email})
        
        if not re.search(r'[A-Z]', password):
            messages.error(request, "Le mot de passe doit contenir au moins une majuscule")
            return render(request, 'nouveauMDP.html', {'email': email})
        
        # Si toutes les validations passent, changer le mot de passe
        user.set_password(password)
        user.save()
        messages.success(request, "Mot de passe changé avec succès")
        return redirect('login')
    
    context = {
        'email': email,
    }
    return render(request, 'nouveauMDP.html', context)

    # fonction pour deconnecter un utilisateur
def Deconnection(request):
    logout(request)
    return redirect('login')