from django.urls import path
from .views import *



urlpatterns = [
    path('connecter/', connecter_compte, name='login'),
    path('creation/', Cration_Compte, name='creation'),
    path('verification/', verification_Mail, name='verification'),
    path('changement_code/<str:email>/', changement_code, name='changement_code'),
]