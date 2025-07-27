from django.urls import path
from .views import *



urlpatterns = [
    path('connecter/', connecter_compte, name='login'),
 
]