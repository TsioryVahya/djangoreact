from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie!')
            
            # Utilisez return redirect('/') au lieu de redirect('home') pour éviter l'erreur
            return redirect('accueil')
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'utilisateurs/login.html')

@login_required
def after_login(request):
    # Redirige vers home.html après la connexion
    return render(request, 'utilisateurs/home.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return redirect('signup')
            
        try:
            user = Utilisateur.objects.create_user(
                nom_utilisateur=username,
                email=email,
                mot_de_passe=password1
            )
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        except Exception as e:
            messages.error(request, str(e))
    
    return render(request, 'utilisateurs/signup.html')
