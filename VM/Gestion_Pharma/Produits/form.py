from .models import Produit, Vente
from django import forms

class AjoutProduitform(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['name', 'categorie', 'price', 'quantite', 'date_expiration', 'description', 'image']
        widgets = { 
            'name': forms.TextInput(attrs={
                'placeholder': 'Entrez le nom du produit',
                'class': 'form-control'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'quantite': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'date_expiration': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Décrivez le produit...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'id': 'id_image',
                'style': 'display: none;'
            }),  
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].error_messages = {
            'required': 'Le nom du produit est obligatoire.',
            'invalid': 'Le nom du produit doit être valide.'
        }
        self.fields['categorie'].error_messages = {
            'required': 'La catégorie est obligatoire.',
            'invalid': 'La catégorie doit être valide.'
        }
        self.fields['price'].error_messages = {
            'required': 'Le prix est obligatoire.', 
            'invalid': 'Le prix doit être un nombre valide.'
        }
        self.fields['quantite'].error_messages = {
            'required': 'La quantité est obligatoire.',   
            'invalid': 'La quantité doit être un nombre valide.'
        }
        self.fields['date_expiration'].error_messages = {
            'required': 'La date d\'expiration est obligatoire.',
            'invalid': 'La date d\'expiration doit être valide.'
        }
        self.fields['description'].error_messages = {
            'required': 'La description est obligatoire.',
            'invalid': 'La description doit être valide.'
        }
        self.fields['image'].error_messages = {
            'required': 'L\'image est obligatoire.',
            'invalid': 'Le fichier doit être une image valide.',
            'invalid_image': 'Le fichier doit être une image valide (JPEG, PNG, GIF).'
        }

# formulaire de vente de produit
from django import forms

class VenteProduitform(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantité",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    customer = forms.CharField(
        max_length=100,
        label="Client",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du client'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].error_messages = {
            'required': 'Le nom du client est obligatoire.',
            'invalid': 'Le nom du client doit être valide.'
        }