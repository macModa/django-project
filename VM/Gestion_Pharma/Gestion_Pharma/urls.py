"""
URL configuration for Gestion_Pharma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from UTILISATEUR.views import connecter_compte, Cration_Compte, verification_Mail, changement_code, Deconnection

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Produits.urls')), 
    path('produits/', include('Produits.urls')),
    path('utilisateur/', include('UTILISATEUR.urls')),
    path('connecter/', connecter_compte, name='login'),
    path('creation/', Cration_Compte, name='creation'),
    path('verification/', verification_Mail, name='verification'),
    path('changement_code/<str:email>/', changement_code, name='changement_code'),
    path('deconnection/', Deconnection, name='deconnection'),
]