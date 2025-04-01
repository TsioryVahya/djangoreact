
from django.urls import path
from . import views

urlpatterns = [
    path('recherche/', views.recherche_view, name='recherche'),
]