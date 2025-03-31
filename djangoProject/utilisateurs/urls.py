from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('accueil/', views.after_login, name='accueil'),
    # Ne pas inclure de chemin vers 'home' ici pour éviter les conflits
]
