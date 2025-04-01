from django.urls import path
from . import views

urlpatterns = [
    path('recherche/', views.recherche_view, name='recherche'),
    # Removed duplicate problemes API endpoint since it's now in main urls.py
]