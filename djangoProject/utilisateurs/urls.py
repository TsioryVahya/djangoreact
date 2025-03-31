from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Chemin explicite pour le login
    path('', views.CustomLoginView.as_view(), name='utilisateurs_home'),  # Page d'accueil des utilisateurs
    path('logout/', views.logout_view, name='logout'),
    path('accueil/', views.AccueilView.as_view(), name='accueil'),
]
